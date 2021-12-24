import React from 'react';
import { Physical, Special, Status } from './IconComponents/index';

function DamageClassIcon(props) {
    switch(props.damageclass){
        case "physical":
            return <Physical {...props}/>;
        case "special":
            return <Special {...props}/>;
        case "status":
            return <Status {...props}/>;
        default:
            return <div />;
    }
}

export default DamageClassIcon;