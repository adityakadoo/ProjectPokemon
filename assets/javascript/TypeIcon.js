import React from 'react';
import { BugTypeIcon, DarkTypeIcon, DragonTypeIcon, ElectricTypeIcon,
         FairyTypeIcon, FightingTypeIcon, FireTypeIcon, FlyingTypeIcon,
         GhostTypeIcon, GrassTypeIcon, GroundTypeIcon, IceTypeIcon,
         NormalTypeIcon, PoisonTypeIcon, PsychicTypeIcon, RockTypeIcon,
         SteelTypeIcon, WaterTypeIcon } from './IconComponents/index';

function TypeIcon(props) {
    switch (props.type) {
        case 'bug':
            return <BugTypeIcon {...props} />
        case 'dark':
            return <DarkTypeIcon {...props} />
        case 'dragon':
            return <DragonTypeIcon {...props} />
        case 'electric':
            return <ElectricTypeIcon {...props} />
        case 'fairy':
            return <FairyTypeIcon {...props} />
        case 'fighting':
            return <FightingTypeIcon {...props} />
        case 'flying':
            return <FlyingTypeIcon {...props} />
        case 'fire':
            return <FireTypeIcon {...props} />
        case 'ghost':
            return <GhostTypeIcon {...props} />
        case 'grass':
            return <GrassTypeIcon {...props} />
        case 'ground':
            return <GroundTypeIcon {...props} />
        case 'ice':
            return <IceTypeIcon {...props} />
        case 'normal':
            return <NormalTypeIcon {...props} />
        case 'poison':
            return <PoisonTypeIcon {...props} />
        case 'psychic':
            return <PsychicTypeIcon {...props} />
        case 'rock':
            return <RockTypeIcon {...props} />
        case 'steel':
            return <SteelTypeIcon {...props} />
        case 'water':
            return <WaterTypeIcon {...props} />
    }
}

export default TypeIcon;