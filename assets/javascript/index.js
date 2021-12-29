import React from 'react';
import ReactDOM from "react-dom";
import ResourceList from './ResourceList';
import Background from './Background';
import '../styles/index.css';

const context = JSON.parse(JSON.parse(document.getElementById('context').textContent));
console.log(context);

function Home(props) {
    return (
        <div id="home" style={{ width: "inherit" }}>
            <Background />
            {/* <div className="page-wrapper"> */}
                <ResourceList parent="root" {...props} />
            {/* </div> */}
        </div>
    );
}

ReactDOM.render(
    <Home resources={context.resources} filters={context.filters} style={{ width: "inherit" }} />,
    document.getElementById('root')
);