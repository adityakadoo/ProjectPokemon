import * as React from "react";

const SvgStatus = (props) => (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    viewBox="0 0 90 90"
    style={{
      filter: "drop-shadow(0 0 0.5em rgba(116 255 0 / .7))",
    }}
    {...props}
  >
    <path d="M36 42v27h16V43.6c0-14-.3-26.1-.6-27-.5-1.3-2.2-1.6-8-1.6H36v27z"
      style={{
        fillRule: "evenodd",
        clipRule: "evenodd",
        fill: "rgb(116 255 0)",
      }}
    />
    <path d="M3 51v30h76v-6H10V21H3v30z"
      style={{
        fillRule: "evenodd",
        clipRule: "evenodd",
        fill: "rgb(116 255 0)",
      }}
    />
    <path d="M57 45v24h16V46.6c0-12.3-.3-23.1-.6-24-.5-1.3-2.2-1.6-8-1.6H57v24zM15 51v18h16V52.6c0-9-.3-17.1-.6-18-.5-1.3-2.2-1.6-8-1.6H15v18z"
      style={{
        fillRule: "evenodd",
        clipRule: "evenodd",
        fill: "rgb(116 255 0)",
      }}
    />
  </svg>
);

export default SvgStatus;
