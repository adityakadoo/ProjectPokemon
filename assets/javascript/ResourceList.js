import React from 'react';
import Card from './Card.js';
import '../styles/resource_list.css';
import { floor, max } from 'lodash';

function elementWidth(id) {
    return document.getElementById(id).clientWidth;
}

function debounce(fn, ms) {
    let timer
    return _ => {
        clearTimeout(timer)
        timer = setTimeout(_ => {
            timer = null
            fn.apply(this, arguments)
        }, ms)
    };
}

function ResourceList(props) {
    const [parentDimension, setDimensions] = React.useState({
        height: 0,
        width: elementWidth(props.parent)
    });
    React.useEffect(() => {
        const debouncedHandleResize = debounce(function handleResize() {
            setDimensions({
                width: elementWidth(props.parent)
            })
        }, 300)

        window.addEventListener('resize', debouncedHandleResize)

        return _ => {
            window.removeEventListener('resize', debouncedHandleResize)

        }
    });
    var numCols = floor((max([parentDimension.width-40, 250]) + 20) / 270);
    var cols = [];
    for (var i = 0; i < numCols; i++) {
        cols.push([]);
    }
    // console.log(parentDimension.width,numCols);

    for (var i = 0; i < props.resources.length; i++) {
        cols[i % numCols].push(
            <div key={"col_" + (i % numCols) + "_item_" + i}>
                <Card resource={props.resources[i]} />
            </div>
        );
    }

    var grid = [];
    for (var i = 0; i < cols.length; i++) {
        grid.push(
            <div className="resource_list_col" key={"col_" + i}>
                {cols[i]}
            </div>
        );
    }

    return (
        <div className="resource_list">
            {grid}
        </div>
    );
}

export default ResourceList;