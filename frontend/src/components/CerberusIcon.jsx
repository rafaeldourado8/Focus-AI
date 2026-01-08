const CerberusIcon = ({ className = "w-6 h-6", animated = false }) => {
  return (
    <svg 
      viewBox="0 0 32 32" 
      fill="none" 
      className={className}
      xmlns="http://www.w3.org/2000/svg"
    >
      {/* Three heads representing Cerberus */}
      <g className={animated ? "animate-pulse" : ""}>
        {/* Left head */}
        <circle cx="8" cy="12" r="4" fill="currentColor" opacity="0.7" />
        <circle cx="8" cy="11" r="1" fill="#ef4444" />
        
        {/* Center head (main) */}
        <circle cx="16" cy="8" r="5" fill="currentColor" />
        <circle cx="16" cy="7" r="1.5" fill="#ef4444" />
        
        {/* Right head */}
        <circle cx="24" cy="12" r="4" fill="currentColor" opacity="0.7" />
        <circle cx="24" cy="11" r="1" fill="#ef4444" />
        
        {/* Body */}
        <path 
          d="M8 16 L16 13 L24 16 L24 24 C24 26 22 28 16 28 C10 28 8 26 8 24 Z" 
          fill="currentColor" 
          opacity="0.5"
        />
      </g>
    </svg>
  );
};

export default CerberusIcon;
