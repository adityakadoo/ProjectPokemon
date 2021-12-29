import React from 'react';
import Card from './Card.js';
import '../styles/resource_list.css';
import { floor, max, min } from 'lodash';
import color_dict from './Resources.js';
import getFilterOptions from './filterOptions.js';
import { components, default as ReactSelect } from "react-select";
import { Search } from './IconComponents/index';

function elementWidth(id) {
    return document.getElementById(id).clientWidth;
}

function elementHeight(id) {
    return document.getElementById(id).clientHeight;
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
                <label style={{
                    padding: "5px",
                    margin: "5px",
                }}>
                    {props.label}
                </label>
                <hr style={{ borderColor: color_dict['dark_txt'] }} />
            </components.Option>
        </div>
    );
};

function ResourceList(props) {
    const [parentDimensions, setDimensions] = React.useState({
        height: elementHeight(props.parent),
        width: elementWidth(props.parent)
    });

    React.useEffect(() => {
        const debouncedHandleResize = debounce(function handleResize() {
            setDimensions({
                width: elementWidth(props.parent),
                height: elementHeight(props.parent)
            })
        }, 300);
        window.addEventListener('resize', debouncedHandleResize);
        return _ => {
            window.removeEventListener('resize', debouncedHandleResize);
        };
    });

    const [listData, setListData] = React.useState(props.resources);
    const [searchWord, setSearchWord] = React.useState("");
    const [pageIndex, setPageIndex] = React.useState(0);
    const pageSize = 60;

    var numCols = min([floor((max([parentDimensions.width - 80, 250]) + 40) / 290), listData.length]);
    var cols = [];
    for (var i = 0; i < numCols; i++) {
        cols.push([]);
    }
    if (numCols != 0) {
        for (var i = 0; i < pageSize; i++) {
            cols[i % numCols].push(
                <div key={"col_" + (i % numCols) + "_item_" + i}>
                    <Card resource={listData[pageIndex * pageSize + i]} />
                </div>
            );
        }
    }
    var grid = [];
    for (var i = 0; i < cols.length; i++) {
        grid.push(
            <div className="resource_list_col" key={"col_" + i}>
                {cols[i]}
            </div>
        );
    }

    const handleSearch = () => {
        var newResources = props.resources.filter((value) => {
            return value.name.includes(searchWord);
        })
        filterSelected.forEach(element => {
            if (element.filter != null)
                newResources = newResources.filter(element.filter);
            if (element.sort != null)
                newResources = newResources.sort(element.sort);
        });
        setListData(newResources);
        setPageIndex(0);
    }

    const [filterSelected, setFilterSelected] = React.useState([]);

    const handleFilter = (event) => {
        var newResources = props.resources.filter((value) => {
            return value.name.includes(searchWord);
        })
        event.forEach(element => {
            if (element.filter != null)
                newResources = newResources.filter(element.filter);
            if (element.sort != null)
                newResources = newResources.sort(element.sort);
        });
        setListData(newResources);
        setFilterSelected(event);
        setPageIndex(0);
    }

    return (
        <div className="resource_list">
            <div className="search_bar" style={{ width: parentDimensions.width }}>
                <div className="search_box" style={{
                    border: "2px solid " + color_dict['dark_txt'],
                    background: color_dict['transparent_bg'],
                }}>
                    <input type="text"
                        className="search_box_input"
                        placeholder="Search a keyword..."
                        onChange={(event) => setSearchWord(event.target.value)}
                        style={{ color: color_dict['dark_txt'] }} />
                    <button className="search_icon"
                        onClick={handleSearch}
                        style={{ background: color_dict['light_mid'], right: "5px", top: "5px", fontSize: "120%" }}>
                        <i className="fas fa-search"></i>
                    </button>
                </div>
                <ReactSelect
                    options={getFilterOptions(props.filters)}
                    isMulti
                    closeMenuOnSelect={false}
                    hideSelectedOptions={false}
                    placeholder="Add a filter or sort..."
                    components={{
                        Option
                    }}
                    onChange={handleFilter}
                    allowSelectAll={true}
                    value={filterSelected}
                    styles={{
                        container: (base) => ({
                            ...base,
                            minWidth: "350px",
                            flexGrow: 1,
                            borderRadius: "25px",
                            boxShadow: "0 0 2em 0.2em #525252"
                        }),
                        control: (base) => ({
                            display: "flex",
                            transition: "all 100ms",
                            flexWrap: "wrap",
                            justifyContent: "space-between",
                            border: "none",
                            background: "transparent",
                            cursor: "text",
                            border: "2px solid " + color_dict['dark_txt'],
                            background: color_dict['transparent_bg'],
                            borderRadius: "25px",
                            minHeight: "50px",
                            padding: "5px",
                            color: color_dict['dark_txt']
                        }),
                        valueContainer: (base) => ({
                            ...base,
                            minHeight: "36px",
                            padding: "0 5px",
                            overflow: "visible",
                            gap: "2px"
                        }),
                        input: (base) => ({
                            ...base,
                            lineHeight: "100%",
                            fontSize: "20px",
                            height: "25px",
                            margin: "0 5px"
                        }),
                        placeholder: (base) => ({
                            ...base,
                            lineHeight: "100%",
                            fontSize: "20px",
                            height: "36px",
                            padding: "8px 0",
                            margin: "0 5px"
                        }),
                        singleValue: (base) => ({
                            ...base,
                            lineHeight: "100%",
                            fontSize: "20px",
                            padding: "4px 25px",
                            height: "36px",
                            minHeight: "36px",
                            margin: "0",
                            zIndex: "-5",
                            color: color_dict['dark_txt']
                        }),
                        menu: (base) => ({
                            ...base,
                            border: "2px solid " + color_dict['dark_txt'],
                            background: color_dict['transparent_txt'],
                            borderRadius: "25px",
                            padding: "10px"
                        }),
                        multiValue: (base) => ({
                            display: "flex",
                            borderRadius: "25px",
                            background: color_dict['light_mid']
                        }),
                        indicatorSeparator: (base) => ({
                            ...base,
                            background: color_dict['transparent_bg'],
                        }),
                        indicatorsContainer: (base) => ({
                            ...base,
                            background: color_dict['light_mid'],
                            borderRadius: "25px"
                        }),
                        clearIndicator: (base) => ({
                            ...base,
                            color: color_dict["transparent_txt"],
                            cursor: "pointer"
                        }),
                        dropdownIndicator: (base) => ({
                            ...base,
                            color: color_dict["transparent_txt"],
                            cursor: "pointer"
                        }),
                        option: (base) => ({
                            borderRadius: "25px",
                            background: "transparent",
                            fontWeight: "700"
                        })
                    }}
                />
                <div className="search_box" style={{
                    border: "2px solid " + color_dict['dark_txt'],
                    background: color_dict['transparent_bg'],
                }}>
                    <button className="search_icon" style={{ left: "5px", top: "5px", fontSize: "120%" }} onClick={() => {
                        if (pageIndex > 0)
                            setPageIndex(pageIndex - 1);
                    }}>
                        <i className="fas fa-angle-left"></i>
                    </button>
                    <div className="search_box_input" style={{ color: color_dict['dark_txt'], margin: "0 40px", padding: "8px 0", textAlign: "center" }}>
                        {(pageIndex * pageSize + 1) + " - " + min([listData.length, (pageIndex + 1) * pageSize + 1]) + " of " + listData.length}
                    </div>
                    <button className="search_icon" style={{ right: "5px", top: "5px", fontSize: "120%" }} onClick={() => {
                        if ((pageIndex + 1) * pageSize < listData.length)
                            setPageIndex(pageIndex + 1);
                    }}>
                        <i className="fas fa-angle-right"></i>
                    </button>
                </div>
            </div>
            <div className="resource_list_main">
                {grid}
            </div>
        </div>
    );
}

export default ResourceList;