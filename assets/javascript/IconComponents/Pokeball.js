import * as React from "react";

const SvgPokeball = (props) => (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    viewBox="0 0 100 100"
    style={{
      filter: props.filter,
    }}
    {...props}
  >
    <circle
      cx={50}
      cy={50}
      r={36}
      style={{
        fill: "#ffffff",
      }}
    />
    <path d="M36 16.2c-7.7 3-16.9 12.3-19.8 20.1-3 7.9-3 19.5 0 27.4 2.9 8 12.1 17.2 20.1 20.1 7.9 3 19.5 3 27.4 0 8-2.9 17.2-12.1 20.1-20.1 3-7.9 3-19.5 0-27.4-2.9-8-12.1-17.2-20.1-20.1-7.8-3-20-2.9-27.7 0zm20.1 27.7c2 2 2.9 3.9 2.9 6.1 0 4.3-4.7 9-9 9s-9-4.7-9-9c0-2.2.9-4.1 2.9-6.1S47.8 41 50 41c2.2 0 4.1.9 6.1 2.9zM40 54.1c1.5 3.6 6.3 6.9 10 6.9s8.5-3.3 10-6.9l1.2-3.1h23.1l-.7 4.2C82 65.7 74.3 75.8 64.2 80.7c-4.9 2.4-6.9 2.8-14.2 2.8-7.2 0-9.3-.4-14-2.7-10.3-5.1-17.9-15-19.6-25.6l-.7-4.2h23.1l1.2 3.1z"
      style={{
        fillRule: "evenodd",
        clipRule: "evenodd",
        fill: "rgb(173 29 29)",
      }}
    />
    <circle
      cx={50}
      cy={50}
      r={9}
      style={{
        fill: "rgb(139 199 255)",
      }}
    />
  </svg>
);

export default SvgPokeball;
