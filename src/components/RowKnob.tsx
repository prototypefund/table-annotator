import {useStore} from "../store";
import React from "react";
import styled from "styled-components";

const RowKnobDiv = styled.div `
    border: 1px solid rgba(0, 0, 0, 8);
    width: 23px;
    height: 20px;
    background: silver;
    position: absolute;
`

type RowKnobProps = {
    position: number
    idx: number
}

const ColumnKnob = ({position, idx} : RowKnobProps) =>{
    const selectRow = useStore(state => state.selectRow)
    const selectedRow = useStore(state => state.selectedRow)

    const handleMouseClick = (e: React.MouseEvent<Element, MouseEvent>) => {
        selectRow(idx)
        e.stopPropagation()
    }


    const isSelected = idx === selectedRow

    return (<RowKnobDiv onClick={handleMouseClick}
                           style={{top: `${position - 10}px`, left: "-30px",
                               cursor: isSelected ? "default" : "pointer"}}/>)
}

export default ColumnKnob