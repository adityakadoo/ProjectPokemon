import React from 'react';
import ReactDOM from "react-dom";
import Card from './Card.js';
import TypeIcon from './TypeIcon';
import color_dict from './Resources.js';
import '../styles/index.css';

const context = JSON.parse(JSON.parse(document.getElementById('context').textContent));
console.log(context);

function List() {
  return (
    <div className="resource_list">
      <Card resource={context.resources[0]} />
      <Card resource={context.resources[1]} />
      <Card resource={context.resources[2]} />
      <Card resource={context.resources[3]} />
      <Card resource={context.resources[4]} />
      <Card resource={context.resources[5]} />
      <Card resource={context.resources[6]} />
      <Card resource={context.resources[11]} />
      <Card resource={context.resources[12]} />
      <Card resource={context.resources[66]} />
      <Card resource={context.resources[67]} />
    </div>
  );
}

ReactDOM.render(
  <List />,
  document.getElementById('root')
);