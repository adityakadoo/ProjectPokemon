import React from 'react';
import ReactDOM from "react-dom";
import ResourceList from './ResourceList';
import '../styles/index.css';

const context = JSON.parse(JSON.parse(document.getElementById('context').textContent));
console.log(context);

ReactDOM.render(
    <ResourceList resources={context.resources} />,
    document.getElementById('root')
);