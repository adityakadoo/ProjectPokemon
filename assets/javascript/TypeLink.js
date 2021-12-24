import React from 'react';
import TypeIcon from './TypeIcon';
import color_dict from './Resources.js';
import '../styles/type_link.css';
import { toUpper } from 'lodash';

class TypeLink extends React.Component {
    constructor(props) {
        super(props);
        this.state = { hover: false };
        this.toggleHover = this.toggleHover.bind(this);
    }

    toggleHover() {
        this.setState({ hover: !this.state.hover });
    }

    render() {
        var temp_col1 = this.state.hover ? color_dict['dark_bg'] : color_dict[this.props.typename];
        var temp_col2 = this.state.hover ? color_dict[this.props.typename] : color_dict['dark_bg'];
        var temp_shadow = this.state.hover ? "0 0 2em 0.5em " + color_dict[this.props.typename] : "inset 0 0 0.5em 0 " + color_dict[this.props.typename] + ", 0 0 0.5em 0 " + color_dict[this.props.typename];
        var temp_text_shadow = this.state.hover ? "none" : "0 0 0.125em hsl(0 0% 100% / 0.3), 0 0 0.45em currentColor";
        return (
            <button onClick={() => window.location.href = "/pokedex/type/" + this.props.typename}
                onMouseEnter={this.toggleHover}
                onMouseLeave={this.toggleHover}
                onFocus={this.toggleHover}
                onBlur={this.toggleHover}
                style={{ textDecoration: 'none' }}
                className="type_link"
                style={{
                    borderColor: color_dict[this.props.typename],
                    backgroundColor: temp_col2,
                    color: temp_col1,
                    border: color_dict[this.props.typename] + " 5px solid",
                    boxShadow: temp_shadow,
                    textShadow: temp_text_shadow
                }}>
                <div className="type_link_icon">
                    <TypeIcon type={this.props.typename}
                        height='35px'
                        col1={color_dict[this.props.typename]}
                        col2={color_dict['dark_bg']}
                        alt={this.props.typename + " icon"} />
                </div>
                <div className="type_link_text">
                    {toUpper(this.props.typename.substring(0, 3))}
                </div>
            </button>
        );
    }
}

export default TypeLink;