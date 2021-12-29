import React from 'react';
import '../styles/background.css';

class Background extends React.Component {
    render() {
        return (
            <div>
                <div className="page-bg"></div>
                <div className="animation-wrapper">
                    <div className="particle particle-1"></div>
                    <div className="particle particle-2"></div>
                    <div className="particle particle-3"></div>
                    <div className="particle particle-4"></div>
                </div>
            </div>
        );
    }
}
export default Background;