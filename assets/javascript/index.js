import React from 'react';
import ReactDOM from "react-dom";
import TypeIcon from './TypeIcon';
import color_dict from './Resources.js';

const context = JSON.parse(JSON.parse(document.getElementById('context').textContent));
console.log(context);

function List() {
  return (
    <div className="resource_list">
      <TypeIcon type='bug' height='200px' col1={color_dict['dark']} col2={color_dict['flying']} />
      <TypeIcon type='dark' height='200px' col1={color_dict['dark']} col2={color_dict['flying']} />
      <TypeIcon type='dragon' height='200px' col1={color_dict['dark']} col2={color_dict['flying']} />
      <TypeIcon type='electric' height='200px' col1={color_dict['dark']} col2={color_dict['flying']} />
      <TypeIcon type='fairy' height='200px' col1={color_dict['dark']} col2={color_dict['flying']} />
      <TypeIcon type='fighting' height='200px' col1={color_dict['dark']} col2={color_dict['flying']} />
      <TypeIcon type='fire' height='200px' col1={color_dict['dark']} col2={color_dict['flying']} />
      <TypeIcon type='flying' height='200px' col1={color_dict['dark']} col2={color_dict['flying']} />
      <TypeIcon type='ghost' height='200px' col1={color_dict['dark']} col2={color_dict['flying']} />
      <TypeIcon type='grass' height='200px' col1={color_dict['dark']} col2={color_dict['flying']} />
      <TypeIcon type='ground' height='200px' col1={color_dict['dark']} col2={color_dict['flying']} />
      <TypeIcon type='ice' height='200px' col1={color_dict['dark']} col2={color_dict['flying']} />
      <TypeIcon type='normal' height='200px' col1={color_dict['dark']} col2={color_dict['flying']} />
      <TypeIcon type='poison' height='200px' col1={color_dict['dark']} col2={color_dict['flying']} />
      <TypeIcon type='psychic' height='200px' col1={color_dict['dark']} col2={color_dict['flying']} />
      <TypeIcon type='rock' height='200px' col1={color_dict['dark']} col2={color_dict['flying']} />
      <TypeIcon type='steel' height='200px' col1={color_dict['dark']} col2={color_dict['flying']} />
      <TypeIcon type='water' height='200px' col1={color_dict['dark']} col2={color_dict['flying']} />
    </div>
  );
}

ReactDOM.render(
  <List />,
  document.getElementById('root')
);