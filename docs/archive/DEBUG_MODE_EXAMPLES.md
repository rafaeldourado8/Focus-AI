# 🐛 Debug Mode - Exemplos Práticos

## Exemplo 1: Debugging de Erro

### ❌ Sem Debug Mode

**Pergunta:**
```
Por que meu código dá TypeError?
```

**Resposta:**
```
Pode ser um problema com variáveis undefined. 
Verifique se os dados estão sendo carregados corretamente.
```

### ✅ Com Debug Mode

**Pergunta:**
```
Por que meu código dá TypeError: Cannot read property 'map' of undefined?

const UserList = ({ users }) => {
  return users.map(user => <div>{user.name}</div>);
};
```

**Resposta:**
```markdown
# 🔍 ANÁLISE DETALHADA

O erro ocorre porque `users` está `undefined` quando o componente renderiza.
Isso acontece em 3 cenários principais:

1. **Prop não passada**: Componente pai não passou a prop
2. **Async data**: Dados ainda não carregados da API
3. **Destructuring incorreto**: Props mal estruturadas

## Stack Trace
```
TypeError: Cannot read property 'map' of undefined
  at UserList (UserList.jsx:2)
  at renderWithHooks (react-dom.js:...)
```

# 🎯 CAUSAS RAIZ

## Causa Mais Provável: Async Data Loading

Quando você faz fetch de dados, há um momento entre:
1. Componente monta (users = undefined)
2. API responde (users = [...])

Durante esse gap, `users.map()` falha.

## Outras Causas Possíveis

- **Prop opcional**: Componente pai pode não passar users
- **API retorna null**: Backend retorna null em vez de []
- **Destructuring errado**: `const { users } = props` mas props.data.users

# 💡 SOLUÇÕES PRÁTICAS

## Solução 1: Optional Chaining + Default Value (Recomendado)

```jsx
const UserList = ({ users = [] }) => {
  return users?.map(user => (
    <div key={user.id}>{user.name}</div>
  ));
};
```

**Trade-offs:**
- ✅ Simples e seguro
- ✅ Funciona com undefined e null
- ⚠️ Renderiza vazio se não houver dados

## Solução 2: Loading State

```jsx
const UserList = ({ users, loading }) => {
  if (loading) return <Spinner />;
  if (!users || users.length === 0) return <EmptyState />;
  
  return users.map(user => (
    <div key={user.id}>{user.name}</div>
  ));
};
```

**Trade-offs:**
- ✅ Melhor UX (mostra loading)
- ✅ Trata caso vazio
- ⚠️ Requer prop adicional

## Solução 3: React Query (Produção)

```jsx
import { useQuery } from '@tanstack/react-query';

const UserList = () => {
  const { data: users = [], isLoading, error } = useQuery({
    queryKey: ['users'],
    queryFn: fetchUsers
  });
  
  if (isLoading) return <Spinner />;
  if (error) return <ErrorMessage error={error} />;
  
  return users.map(user => (
    <div key={user.id}>{user.name}</div>
  ));
};
```

**Trade-offs:**
- ✅ Cache automático
- ✅ Retry logic
- ✅ Stale-while-revalidate
- ⚠️ Dependência externa

# ✅ MELHORES PRÁTICAS

## 1. Sempre Use Keys em Lists
```jsx
// ❌ Ruim
users.map(user => <div>{user.name}</div>)

// ✅ Bom
users.map(user => <div key={user.id}>{user.name}</div>)
```

## 2. TypeScript para Type Safety
```typescript
interface User {
  id: string;
  name: string;
}

interface UserListProps {
  users?: User[];
  loading?: boolean;
}

const UserList: React.FC<UserListProps> = ({ users = [], loading = false }) => {
  // TypeScript garante que users é array
};
```

## 3. PropTypes (se não usar TS)
```jsx
import PropTypes from 'prop-types';

UserList.propTypes = {
  users: PropTypes.arrayOf(PropTypes.shape({
    id: PropTypes.string.isRequired,
    name: PropTypes.string.isRequired
  })),
  loading: PropTypes.bool
};

UserList.defaultProps = {
  users: [],
  loading: false
};
```

## 4. Error Boundaries
```jsx
class ErrorBoundary extends React.Component {
  state = { hasError: false };
  
  static getDerivedStateFromError(error) {
    return { hasError: true };
  }
  
  render() {
    if (this.state.hasError) {
      return <ErrorFallback />;
    }
    return this.props.children;
  }
}

// Uso
<ErrorBoundary>
  <UserList users={users} />
</ErrorBoundary>
```

# 🏗️ ARQUITETURA & ESCALABILIDADE

## Pattern: Container/Presenter

```jsx
// Container (lógica)
const UserListContainer = () => {
  const { data, loading, error } = useUsers();
  
  return (
    <UserListPresenter 
      users={data} 
      loading={loading} 
      error={error} 
    />
  );
};

// Presenter (UI)
const UserListPresenter = ({ users = [], loading, error }) => {
  if (loading) return <Spinner />;
  if (error) return <ErrorMessage error={error} />;
  if (users.length === 0) return <EmptyState />;
  
  return users.map(user => <UserCard key={user.id} user={user} />);
};
```

## Escalabilidade: Virtualização

Para listas grandes (1000+ items):

```jsx
import { FixedSizeList } from 'react-window';

const UserList = ({ users = [] }) => (
  <FixedSizeList
    height={600}
    itemCount={users.length}
    itemSize={50}
    width="100%"
  >
    {({ index, style }) => (
      <div style={style}>
        {users[index].name}
      </div>
    )}
  </FixedSizeList>
);
```

## Considerações de Produção

1. **Pagination**: Não carregue todos os usuários de uma vez
2. **Infinite Scroll**: Use react-infinite-scroll-component
3. **Search/Filter**: Implemente no backend, não no frontend
4. **Cache**: Use React Query ou SWR
5. **Monitoring**: Sentry para capturar erros em produção

---
🔧 Debug Info: Model=`gemini-2.5-pro-debug` | Senior=`true`
```

---

## Exemplo 2: Otimização de Performance

### ❌ Sem Debug Mode

**Pergunta:**
```
Meu componente React está lento
```

**Resposta:**
```
Tente usar React.memo() para evitar re-renders desnecessários.
```

### ✅ Com Debug Mode

**Pergunta:**
```
Meu componente React está lento. Renderiza 1000 items e trava ao digitar.

const List = ({ items, onSearch }) => {
  const [query, setQuery] = useState('');
  
  const filtered = items.filter(item => 
    item.name.toLowerCase().includes(query.toLowerCase())
  );
  
  return (
    <>
      <input value={query} onChange={e => setQuery(e.target.value)} />
      {filtered.map(item => <Item key={item.id} data={item} />)}
    </>
  );
};
```

**Resposta:**
```markdown
# 🔍 ANÁLISE DETALHADA

Você tem 3 problemas de performance combinados:

1. **Re-render em cada keystroke**: Toda digitação re-renderiza 1000 items
2. **Filter síncrono**: Bloqueia thread principal
3. **Sem virtualização**: Renderiza todos os 1000 items no DOM

## Profiling
```
Render time: ~500ms por keystroke
Main thread blocked: 450ms
Items in DOM: 1000
Memory: ~50MB
```

# 🎯 CAUSAS RAIZ

## 1. Filter Síncrono Bloqueante

```javascript
// Executa a CADA keystroke
const filtered = items.filter(item => 
  item.name.toLowerCase().includes(query.toLowerCase())
);
```

Com 1000 items:
- 1000 iterações
- 1000 toLowerCase() calls
- 1000 includes() checks
= ~450ms bloqueado

## 2. Re-render de Todos os Items

Mesmo items que não mudaram são re-renderizados porque:
- Componente pai re-renderiza
- Items não são memoizados
- Props são recriadas

## 3. DOM Overload

1000 elementos no DOM:
- Layout thrashing
- Paint/Composite lento
- Scroll janky

# 💡 SOLUÇÕES PRÁTICAS

## Solução 1: Debounce + useMemo (Rápido)

```jsx
import { useState, useMemo } from 'react';
import { useDebounce } from 'use-debounce';

const List = ({ items }) => {
  const [query, setQuery] = useState('');
  const [debouncedQuery] = useDebounce(query, 300);
  
  const filtered = useMemo(() => {
    if (!debouncedQuery) return items;
    
    const lowerQuery = debouncedQuery.toLowerCase();
    return items.filter(item => 
      item.name.toLowerCase().includes(lowerQuery)
    );
  }, [items, debouncedQuery]);
  
  return (
    <>
      <input 
        value={query} 
        onChange={e => setQuery(e.target.value)} 
      />
      {filtered.map(item => (
        <MemoizedItem key={item.id} data={item} />
      ))}
    </>
  );
};

const MemoizedItem = React.memo(({ data }) => (
  <div>{data.name}</div>
));
```

**Resultado:**
- ✅ Input responsivo (sem lag)
- ✅ Filter só executa após 300ms
- ✅ Items memoizados
- ⚠️ Ainda renderiza todos no DOM

## Solução 2: Virtualização (Recomendado)

```jsx
import { FixedSizeList } from 'react-window';
import { useDebounce } from 'use-debounce';

const List = ({ items }) => {
  const [query, setQuery] = useState('');
  const [debouncedQuery] = useDebounce(query, 300);
  
  const filtered = useMemo(() => {
    if (!debouncedQuery) return items;
    const lowerQuery = debouncedQuery.toLowerCase();
    return items.filter(item => 
      item.name.toLowerCase().includes(lowerQuery)
    );
  }, [items, debouncedQuery]);
  
  return (
    <>
      <input 
        value={query} 
        onChange={e => setQuery(e.target.value)} 
      />
      <FixedSizeList
        height={600}
        itemCount={filtered.length}
        itemSize={50}
        width="100%"
      >
        {({ index, style }) => (
          <div style={style}>
            {filtered[index].name}
          </div>
        )}
      </FixedSizeList>
    </>
  );
};
```

**Resultado:**
- ✅ Renderiza apenas ~15 items visíveis
- ✅ Scroll suave (60fps)
- ✅ Memória reduzida (5MB vs 50MB)
- ✅ Funciona com 10,000+ items

## Solução 3: Web Worker (Produção)

```jsx
// worker.js
self.addEventListener('message', (e) => {
  const { items, query } = e.data;
  const lowerQuery = query.toLowerCase();
  
  const filtered = items.filter(item => 
    item.name.toLowerCase().includes(lowerQuery)
  );
  
  self.postMessage(filtered);
});

// Component
const List = ({ items }) => {
  const [query, setQuery] = useState('');
  const [filtered, setFiltered] = useState(items);
  const workerRef = useRef(null);
  
  useEffect(() => {
    workerRef.current = new Worker('worker.js');
    workerRef.current.onmessage = (e) => setFiltered(e.data);
    return () => workerRef.current.terminate();
  }, []);
  
  const handleSearch = useCallback((value) => {
    setQuery(value);
    workerRef.current.postMessage({ items, query: value });
  }, [items]);
  
  return (
    <>
      <input value={query} onChange={e => handleSearch(e.target.value)} />
      <VirtualList items={filtered} />
    </>
  );
};
```

**Resultado:**
- ✅ Main thread nunca bloqueia
- ✅ Input sempre responsivo
- ✅ Filter em background
- ⚠️ Complexidade maior

# ✅ MELHORES PRÁTICAS

## 1. Profile Antes de Otimizar

```jsx
import { Profiler } from 'react';

<Profiler id="List" onRender={(id, phase, actualDuration) => {
  console.log(`${id} (${phase}) took ${actualDuration}ms`);
}}>
  <List items={items} />
</Profiler>
```

## 2. Use React DevTools Profiler

1. Abra DevTools
2. Tab "Profiler"
3. Click "Record"
4. Interaja com o app
5. Analise flamegraph

## 3. Lazy Loading

```jsx
const Item = lazy(() => import('./Item'));

<Suspense fallback={<Skeleton />}>
  <Item data={data} />
</Suspense>
```

## 4. Code Splitting

```jsx
const HeavyComponent = lazy(() => import('./HeavyComponent'));

// Só carrega quando necessário
{showHeavy && (
  <Suspense fallback={<Spinner />}>
    <HeavyComponent />
  </Suspense>
)}
```

# 🏗️ ARQUITETURA & ESCALABILIDADE

## Pattern: Server-Side Search

```jsx
// Backend faz o filter
const List = () => {
  const [query, setQuery] = useState('');
  const [debouncedQuery] = useDebounce(query, 300);
  
  const { data: items = [] } = useQuery({
    queryKey: ['items', debouncedQuery],
    queryFn: () => fetchItems({ search: debouncedQuery })
  });
  
  return (
    <>
      <input value={query} onChange={e => setQuery(e.target.value)} />
      <VirtualList items={items} />
    </>
  );
};
```

## Benchmarks

| Solução | Render Time | Memory | Scroll FPS |
|---------|-------------|--------|------------|
| Original | 500ms | 50MB | 15fps |
| Debounce + Memo | 50ms | 45MB | 30fps |
| Virtualização | 10ms | 5MB | 60fps |
| Web Worker | 5ms | 5MB | 60fps |

## Considerações de Produção

1. **Pagination**: Carregue 50 items por vez
2. **Infinite Scroll**: Use react-infinite-scroll-component
3. **CDN**: Cache de dados estáticos
4. **IndexedDB**: Cache local para offline
5. **Service Worker**: Background sync

---
🔧 Debug Info: Model=`gemini-2.5-pro-debug` | Senior=`true`
```

---

## Mais Exemplos

- [Debugging SQL N+1](./examples/sql-n-plus-1.md)
- [Memory Leak Detection](./examples/memory-leak.md)
- [API Rate Limiting](./examples/rate-limiting.md)
- [Docker Optimization](./examples/docker-optimization.md)
- [Security Vulnerabilities](./examples/security-audit.md)

---

**Ative o Debug Mode e turbine seu desenvolvimento! 🚀**
