import React from 'react';
import Card from './Card.js';
import '../styles/resource_list.css';
import { floor, max } from 'lodash';
import color_dict from './Resources.js';
import { components, default as ReactSelect } from "react-select";

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

function Option(props) {
    return (
        <div>
            <components.Option {...props}>
                <input
                    type="checkbox"
                    checked={props.isSelected}
                    onChange={() => null}
                />{" "}
                <label>{props.label}</label>
            </components.Option>
        </div>
    );
};

const filterOptions = [
    { value: "end-pokemon", label: "Only Pokemon" },
    { value: "end-move", label: "Only moves" },
    { value: "end-type", label: "Only types" },
    { value: "end-ability", label: "Only abilities" },
];

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

    const [searchData, setSearchData] = React.useState(props.resources);

    var numCols = floor((max([parentDimension.width - 80, 250]) + 40) / 290);
    var cols = [];
    for (var i = 0; i < numCols; i++) {
        cols.push([]);
    }
    for (var i = 0; i < searchData.length; i++) {
        cols[i % numCols].push(
            <div key={"col_" + (i % numCols) + "_item_" + i}>
                <Card resource={searchData[i]} />
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

    const handleSearch = (event) => {
        const searchWord = event.target.value
        const newResources = props.resources.filter((value) => {
            return value.name.includes(searchWord);
        })
        setSearchData(newResources);
    }

    const [filterSelected, setFilterSelected] = React.useState(null);

    return (
        <div className="resource_list">
            <div className="search_bar" style={{ width: parentDimension.width }}>
                <div className="search_box" style={{ border: "2px solid " + color_dict['dark_txt'], background: color_dict['dark_bg'] }}>
                    <input type="text"
                        className="search_box_input"
                        placeholder="Search a keyword.."
                        onChange={handleSearch}
                        style={{color: color_dict['dark_txt']}} />
                </div>
                {/* <div className="filter_sort_box" style={{  }}> */}
                {/* <input type="text" className="filter_sort_box_input" placeholder="Add a filter.." /> */}
                <ReactSelect
                    options={filterOptions}
                    isMulti
                    closeMenuOnSelect={false}
                    hideSelectedOptions={false}
                    placeholder="Add a filter"
                    components={{
                        Option
                    }}
                    onChange={setFilterSelected}
                    allowSelectAll={true}
                    value={filterSelected}
                    styles={{
                        container: (base) => ({
                            ...base,
                            flexGrow: "2",
                        }),
                        control: (base) => ({
                            display: "flex",
                            transition: "all 100ms",
                            flexWrap: "wrap",
                            justifyContent: "space-between",
                            border: "none",
                            background: "transparent",
                            cursor: "crosshair",
                            border: "2px solid " + color_dict['dark_txt'],
                            background: color_dict['dark_bg'],
                            height: "50px",
                            borderRadius: "25px",
                            padding: "5px"
                        }),
                        valueContainer: (base) => ({
                            height: "36px"
                        }),
                        input: (base) => ({
                            ...base,
                            lineHeight: "100%",
                            fontSize: "30px",
                            padding: "0 25px",
                            height: "36px",
                            minHeight: "36px",
                            margin: "0",
                            position: "absolute",
                            top: "4px",
                            color: color_dict['dark_txt']
                        }),
                        placeholder: (base) => ({
                            ...base,
                            lineHeight: "100%",
                            fontSize: "30px",
                            padding: "4px 25px",
                            height: "36px",
                            minHeight: "36px",
                            margin: "0",
                            zIndex: "-5"
                        })
                    }}
                />
                {/* </div> */}
            </div>
            <div className="resource_list_main">
                {grid}
            </div>
        </div>
    );
}

export default ResourceList;