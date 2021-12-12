import React from 'react';
import ReactDOM from "react-dom";

const context = JSON.parse(JSON.parse(document.getElementById('context').textContent));
console.log(context)

ReactDOM.render(
  <h1>Hello, { context.endpoints[0] }</h1>,
  document.getElementById('root')
);