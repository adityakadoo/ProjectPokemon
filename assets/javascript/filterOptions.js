import { filter, random, toUpper } from 'lodash';

const getFilterOptions = (filters) => {
    var filterOptions = [
        {
            value: "serial",
            label: "Sort: By index values",
            filter: null,
            sort: (value1, value2) => {
                return value1.index - value2.index;
            }
        },
        {
            value: "alphabetical",
            label: "Sort: Alphabetically",
            filter: null,
            sort: (value1, value2) => {
                return value1.name.localeCompare(value2.name);
            }
        },
        {
            value: "random",
            label: "Sort: Random Order",
            filter: null,
            sort: (value1, value2) => {
                return 2 * random(0, 1, false) - 1;
            }
        }
    ];
    filters.pokedexes.forEach(element => {
        filterOptions.push({
            value: "pokedex-" + element.name,
            label: "Pokedex: " + toUpper(element.name),
            filter: (value) => {
                if (value.endpoint == "pokemon")
                    return element.pokemons.includes(value.name);
                else
                    return false;
            },
            sort: (value1, value2) => {
                const index1 = element.pokemons.findIndex((entry) => {
                    return entry==value1.name
                });
                const index2 = element.pokemons.findIndex((entry) => {
                    return entry==value2.name
                });
                return  index1 - index2;
            }
        })
    });
    filters.endpoints.forEach(element => {
        filterOptions.push({
            value: "end-" + element,
            label: "Filter: Only " + toUpper(element),
            filter: (value) => {
                return value.endpoint == element;
            },
            sort: null
        })
    });
    filters.types.forEach(element => {
        filterOptions.push({
            value: "type-" + element,
            label: "Filter: Only " + toUpper(element) + " types",
            filter: (value) => {
                switch (value.endpoint) {
                    case "pokemon":
                        return value.data.types.includes(element);
                    case "type":
                        return value.name == element;
                    case "move":
                        return value.data.type == element;
                    default:
                        return false;
                }
            },
            sort: null
        });
    });
    return filterOptions;
}

export default getFilterOptions;