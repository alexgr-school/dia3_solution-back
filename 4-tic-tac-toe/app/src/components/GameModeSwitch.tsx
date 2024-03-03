import React from 'react';
import { Switch } from './ui/switch';
import { Label } from './ui/label';

type GameModeSwitchProps = {
    checked: boolean;
    onChange: (checked: boolean) => void;
};

const GameModeSwitch = ({ checked = false, onChange }: GameModeSwitchProps) => {
    return (
        <div className="flex items-center space-x-2">
            <Label htmlFor="game-mode">PvP</Label>
            <Switch
                id="game-mode"
                checked={checked}
                onCheckedChange={onChange}
            />
            <Label htmlFor="game-mode">PvE</Label>
        </div>
    );
};

export default GameModeSwitch;
