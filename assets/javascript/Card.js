import { toUpper } from 'lodash';
import React from 'react';
import "../styles/card.css";
import color_dict from './Resources';
import TypeIcon from './TypeIcon';
import DamageClassIcon from './DamageClassIcon';
import TypeLink from './TypeLink';
import { OpenPokeball, Pokeball } from './IconComponents/index';

function PokemonContent(props) {
    if (props.resource.data.types.length == 2) {
        return (
            <div className='card_content' style={{ backgroundImage: "linear-gradient(transparent 50%, " + color_dict['transparent_bg'] + " 80%), url(.." + props.resource.imageURL + ")", paddingTop: "76%" }}>
                <div style={{ display: 'flex', flexDirection: 'row' }}>
                    <TypeLink typename={props.resource.data.types[0]} />
                    <TypeLink typename={props.resource.data.types[1]} />
                </div>
            </div>
        );
    }
    else if (props.resource.data.types.length == 1) {
        return (
            <div className='card_content' style={{ backgroundImage: "linear-gradient(transparent 50%, " + color_dict['transparent_bg'] + " 80%), url(.." + props.resource.imageURL + ")", paddingTop: "76%" }}>
                <div style={{ display: 'flex', flexDirection: 'row' }}>
                    <TypeLink typename={props.resource.data.types[0]} />
                </div>
            </div>
        );
    }
}

function MoveContent(props) {
    return (
        <div className='card_content'>
            <div style={{ display: 'flex', flexDirection: 'column' }}>
                <div style={{ padding: "0 20%" }}>
                    <table style={{ width: '100%', height: '90px' }}>
                        <tbody>
                            <tr style={{ height: '50%' }}>
                                <td style={{ width: '50%', textAlign: 'left' }}>Power</td>
                                <td style={{ width: '50%', textAlign: 'right' }}>{props.resource.data.power == null ? "--" : props.resource.data.power}</td>
                            </tr>
                            <tr style={{ height: '50%' }}>
                                <td style={{ textAlign: 'left' }}>Accuracy</td>
                                <td style={{ textAlign: 'right' }}>{props.resource.data.accuracy == null ? "--" : props.resource.data.accuracy}</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
                <div style={{ display: 'flex', flexDirection: 'row' }}>
                    <TypeLink typename={props.resource.data.type} />
                    <div style={{ padding: "0 20%" }}>
                        <DamageClassIcon damageclass={props.resource.data.damage_class} height="50px" />
                    </div>
                </div>
            </div>
        </div>
    );
}

function TypeContent(props) {
    return (
        <div className='card_content' style={{ maxHeight: "80%", overflow: "hidden", paddingLeft: "12%" }}>
            <TypeIcon type={props.resource.name}
                alt={props.resource.name + " image"}
                width='100%'
                col1={color_dict[props.resource.name]}
                col2={color_dict['transparent_txt']} />
        </div>
    );
}

class Card extends React.Component {
    constructor(props) {
        super(props);
        this.state = { hover: false };
        this.setHoverOff = this.setHoverOff.bind(this);
        this.setHoverOn = this.setHoverOn.bind(this);
    }

    setHoverOff() {
        this.setState({ hover: false });
    }

    setHoverOn() {
        this.setState({ hover: true });
    }

    render() {
        try {
            var type_col = [color_dict['dark_mid'], color_dict['dark_mid']];
            var content = <div />;
            var grid_rows = 2;
            switch (this.props.resource.endpoint) {
                case "pokemon":
                    if (this.props.resource.data !== null) {
                        if (this.props.resource.data.types.length === 2) {
                            type_col = [color_dict[this.props.resource.data.types[0]], color_dict[this.props.resource.data.types[1]]];
                        }
                        else if (this.props.resource.data.types.length === 1) {
                            type_col = [color_dict[this.props.resource.data.types[0]], color_dict[this.props.resource.data.types[0]]];
                        }
                        content = <PokemonContent resource={this.props.resource} />
                        grid_rows = 7;
                    }
                    break;
                case "move":
                    if (this.props.resource.data !== null) {
                        type_col = [color_dict[this.props.resource.data.type], color_dict[this.props.resource.data.type]];
                        content = <MoveContent resource={this.props.resource} />
                        grid_rows = 5;
                    }
                    break;
                case "type":
                    type_col = [color_dict[this.props.resource.name], color_dict[this.props.resource.name]];
                    content = <TypeContent resource={this.props.resource} />
                    grid_rows = 6;
                    break;
                default:
                    break;
            }
            var header_icon = this.state.hover ? <Pokeball height="70px" width="140%" filter="drop-shadow(0 0 2em rgba(173 29 29 / .7))" /> : <Pokeball height="70px" width="140%" filter="drop-shadow(0 0 0.5em rgba(173 29 29 / .7))" />;
            return (
                <div className="card" style={{ background: color_dict['transparent_bg'] }}>
                    <div className="card_header"
                        style={{
                            textDecoration: 'none',
                            color: color_dict['transparent_txt'],
                            background: 'linear-gradient(to right, ' + type_col[0] + ' 45%, ' + type_col[1] + ' 55%)'
                        }}>
                        <div className="card_header_endpoint">
                            {toUpper(this.props.resource.endpoint)}
                        </div>
                        <a href={"/pokedex/" + this.props.resource.endpoint + "/" + this.props.resource.name}
                            onMouseEnter={this.setHoverOn}
                            onMouseLeave={this.setHoverOff}
                            onFocus={this.setHoverOn}
                            onBlur={this.setHoverOff}
                            onTouchStart={this.setHoverOn}
                            onTouchEnd={this.setHoverOff}
                            className="card_header_icon">
                            {header_icon}
                        </a>
                        <div className="card_header_index">
                            #{this.props.resource.index}
                        </div>
                    </div>
                    <div className="card_title" style={{ color: color_dict['dark_txt'] }}>
                        {toUpper(this.props.resource.name)}
                    </div>
                    {content}
                </div>
            );
        } catch (e) {
            return <div />;
        }
    }
}

export default Card;