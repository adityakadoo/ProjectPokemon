import React from 'react';
import Card from './Card.js';
import '../styles/resource_list.css';

function ResourceList(props) {
    return (
        <div className="resource_list">
            <Card resource={props.resources[0]} />
            <Card resource={props.resources[1]} />
            <Card resource={props.resources[2]} />
            <Card resource={props.resources[3]} />
            <Card resource={props.resources[4]} />
            <Card resource={props.resources[5]} />
            <Card resource={props.resources[6]} />
            <Card resource={props.resources[11]} />
            <Card resource={props.resources[15]} />
            <Card resource={props.resources[23]} />
            <Card resource={props.resources[66]} />
            <Card resource={props.resources[67]} />
        </div>
    );
}

export default ResourceList;