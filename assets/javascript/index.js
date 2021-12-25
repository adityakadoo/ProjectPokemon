import React from 'react';
import ReactDOM from "react-dom";
import ResourceList from './ResourceList';
import '../styles/index.css';

const context = JSON.parse(JSON.parse(document.getElementById('context').textContent));
console.log(context);

function Home(props) {
    return (
        <div id="home" style={{ width: "inherit" }}>
            <ResourceList parent="root" {...props} />
        </div>
    );
}

ReactDOM.render(
    <Home resources={context.resources} style={{ width: "inherit" }} />,
    document.getElementById('root')
);