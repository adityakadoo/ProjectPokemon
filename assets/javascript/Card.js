import { toUpper } from 'lodash';
import React from 'react';
import "../styles/card.css";
import color_dict from './Resources';
import TypeIcon from './TypeIcon';
import TypeLink from './TypeLink';

function PokemonContent(props) {
    if (props.resource.data.types.length == 2) {
        return (
            <div className='card_content'>
                <img src={".." + props.resource.imageURL} alt={props.resource.name + " image"} style={{ width: '246px' }} />
                <div style={{ display: 'flex', flexDirection: 'row', width: '228px', height: '54px' }}>
                    <div style={{ flex: '104px', margin: '5px' }}>
                        <TypeLink typename={props.resource.data.types[0]} />
                    </div>
                    <div style={{ flex: '104px', margin: '5px' }}>
                        <TypeLink typename={props.resource.data.types[1]} />
                    </div>
                </div>
            </div>
        );
    }
    else if (props.resource.data.types.length == 1) {
        return (
            <div className='card_content'>
                <img src={".." + props.resource.imageURL} alt={props.resource.name + " image"} style={{ width: '246px' }} />
                <div style={{ display: 'flex', flexDirection: 'row', width: '228px', height: '54px' }}>
                    <div style={{ flex: '104px', margin: '5px' }}>
                        <TypeLink typename={props.resource.data.types[0]} />
                    </div>
                </div>
            </div>
        );
    }
}

function MoveContent(props) {
    return (
        <div className='card_content'>
            <div style={{ display: 'flex', flexDirection: 'column', width: '250px', height: '154px' }}>
                <div>
                    <table style={{ width: '250px', height: '100px' }}>
                        <tbody>
                            <tr style={{ height: '50%' }}>
                                <td style={{ width: '45%' }}>Power</td>
                                <td style={{ width: '40%' }}>-</td>
                                <td style={{ width: '15%' }}>{props.resource.data.power.latest}</td>
                            </tr>
                            <tr style={{ height: '50%' }}>
                                <td>Accuracy</td>
                                <td>-</td>
                                <td>{props.resource.data.power.latest}</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
                <div style={{ flex: '104px', margin: '5px', display: 'flex', flexDirection: 'row' }}>
                    <div style={{ flex: '114px' }}>
                        <TypeLink typename={props.resource.data.type} />
                    </div>
                    <div style={{ flex: '116px', textAlign: 'right', fontSize: '30px', padding: '5px' }}>
                        {toUpper(props.resource.data.damage_class.substring(0, 3))}
                    </div>
                </div>
            </div>
        </div>
    );
}

function TypeContent(props) {
    return (
        <div className='card_content'>
            <TypeIcon type={props.resource.name}
                alt={props.resource.name + " image"}
                width='246px'
                col1={color_dict[props.resource.name]}
                col2={color_dict['dark_bg']} />
        </div>
    );
}

class Card extends React.Component {
    constructor(props) {
        super(props);
        this.state = { hover: false };
        this.toggleHover = this.toggleHover.bind(this);
    }

    toggleHover() {
        this.setState({ hover: !this.state.hover });
    }

    render() {
        var type_col = ["#777777", "#777777"];
        var content = <div />;
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
                }
                break;
            case "move":
                if (this.props.resource.data !== null) {
                    type_col = [color_dict[this.props.resource.data.type], color_dict[this.props.resource.data.type]];
                    content = <MoveContent resource={this.props.resource} />
                }
                break;
            case "type":
                type_col = [color_dict[this.props.resource.name], color_dict[this.props.resource.name]];
                content = <TypeContent resource={this.props.resource} />
                break;
            default:
                break;
        }
        var link_color = this.state.hover ? type_col[0] : 'inherit';
        return (
            <a href={"/pokedex/" + this.props.resource.endpoint + "/" + this.props.resource.index}
                onMouseEnter={this.toggleHover}
                onMouseLeave={this.toggleHover}
                style={{ textDecoration: 'none', color: 'inherit' }}>
                <div className="card_outer" style={{ background: 'linear-gradient(' + type_col[0] + ',' + type_col[1] + ')' }}>
                    <div className="card_inner" style={{ background: color_dict['dark_bg'] }}>
                        <div className="card_header" style={{color: link_color}}>
                            <div className="card_header_enpoint">
                                {toUpper(this.props.resource.endpoint)}
                            </div>
                            <div className="card_header_index">
                                #{this.props.resource.index}
                            </div>
                        </div>
                        <hr style={{ visibility: 'hidden' }} />
                        <div className="card_title" style={{color: link_color}}>
                            {toUpper(this.props.resource.name)}
                        </div>
                        {content}
                    </div>
                </div>
            </a>
        );
    }
}

export default Card;