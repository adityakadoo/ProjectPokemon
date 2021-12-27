import React from 'react';
import Card from './Card.js';
import '../styles/resource_list.css';
import { floor, max, random } from 'lodash';
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
    {
        value: "random",
        label: "Sort: Random Order",
        filter: (value) => {
            return true;
        },
        sort: (value1, value2) => {
            return 2 * random(0, 1, false) - 1;
        }
    },
    {
        value: "default",
        label: "Sort: Type and Index",
        filter: (value) => {
            return true;
        },
        sort: (value1, value2) => {
            const endpoint_ordering = {
                "pokemon": 1,
                "move": 2,
                "type": 3,
                "ability": 4,
                "version": 5,
                "version-group": 6,
                "pokedex": 7
            }
            if (value1.endpoint == value2.endpoint) {
                return value1.index - value2.index;
            }
            return endpoint_ordering[value1.endpoint] - endpoint_ordering[value2.endpoint];
        }
    },
    {
        value: "end-pokemon",
        label: "Filter: Only Pokemon",
        filter: (value) => {
            return value.endpoint == "pokemon";
        },
        sort: (value1, value2) => {
            return value1.index - value2.index;
        }
    },
    {
        value: "end-move",
        label: "Filter: Only Moves",
        filter: (value) => {
            return value.endpoint == "move";
        },
        sort: (value1, value2) => {
            return value1.index - value2.index;
        }
    },
    {
        value: "end-type",
        label: "Filter: Only Types",
        filter: (value) => {
            return value.endpoint == "type";
        },
        sort: (value1, value2) => {
            return value1.index - value2.index;
        }
    },
    {
        value: "end-ability",
        label: "Filter: Only Abilities",
        filter: (value) => {
            return value.endpoint == "ability";
        },
        sort: (value1, value2) => {
            return value1.index - value2.index;
        }
    },
    {
        value: "type-fire",
        label: "Filter: Only Fire Types",
        filter: (value) => {
            switch (value.endpoint) {
                case "pokemon":
                    return value.data.types.includes("fire");
                case "type":
                    return value.name == "fire";
                case "move":
                    return value.data.type == "fire";
                default:
                    return false;
            }
        },
        sort: (value1, value2) => {
            const endpoint_ordering = {
                "pokemon": 2,
                "move": 3,
                "type": 1,
            }
            if (value1.endpoint == value2.endpoint) {
                return value1.index - value2.index;
            }
            return endpoint_ordering[value1.endpoint] - endpoint_ordering[value2.endpoint];
        }
    }
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

    const [listData, setListData] = React.useState(props.resources);

    var numCols = floor((max([parentDimension.width - 80, 250]) + 40) / 290);
    var cols = [];
    for (var i = 0; i < numCols; i++) {
        cols.push([]);
    }
    for (var i = 0; i < 60; i++) {
        cols[i % numCols].push(
            <div key={"col_" + (i % numCols) + "_item_" + i}>
                <Card resource={listData[i]} />
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
        const searchWord = event.target.value;
        const newResources = props.resources.filter((value) => {
            return value.name.includes(searchWord);
        })
        setListData(newResources);
    }

    const [filterSelected, setFilterSelected] = React.useState(null);

    const handleFilter = (event) => {
        const newResources = props.resources.filter(event.filter).sort(event.sort);
        setListData(newResources);
        setFilterSelected(event);
    }

    return (
        <div className="resource_list">
            <div className="search_bar" style={{ width: parentDimension.width }}>
                <div className="search_box" style={{
                    border: "2px solid " + color_dict['dark_bg'],
                    background: color_dict['dark_txt'],
                }}>
                    <input type="text"
                        className="search_box_input"
                        placeholder="Search a keyword.."
                        onChange={handleSearch}
                        style={{ color: color_dict['dark_bg'] }} />
                </div>
                {/* <div className="filter_sort_box" style={{  }}> */}
                {/* <input type="text" className="filter_sort_box_input" placeholder="Add a filter.." /> */}
                <ReactSelect
                    options={filterOptions}
                    closeMenuOnSelect={false}
                    hideSelectedOptions={false}
                    placeholder="Add a filter"
                    components={{
                        Option
                    }}
                    onChange={handleFilter}
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
                            border: "2px solid " + color_dict['dark_bg'],
                            background: color_dict['dark_txt'],
                            borderRadius: "25px",
                            height: "50px",
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
                            color: color_dict['dark_bg']
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
                        }),
                        singleValue: (base) => ({
                            ...base,
                            lineHeight: "100%",
                            fontSize: "30px",
                            padding: "4px 25px",
                            height: "36px",
                            minHeight: "36px",
                            margin: "0",
                            zIndex: "-5",
                            color: color_dict['dark_bg']
                        }),
                        menu: (base) => ({
                            ...base,
                            border: "2px solid " + color_dict['dark_bg'],
                            background: color_dict['dark_txt'],
                            borderRadius: "25px",
                            padding: "10px",
                            color: color_dict['dark_bg']
                        }),
                        indicatorSeparator: (base) => ({
                            ...base,
                            background: color_dict['dark_tbg'],
                        }),
                        indicatorsContainer: (base) => ({
                            ...base,
                            color: color_dict['dark_tbg'],
                        }),
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