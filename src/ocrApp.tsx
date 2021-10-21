import React, {useEffect} from 'react';
import create from 'zustand'
import { GlobalHotKeys } from "react-hotkeys";
import axios from 'axios';
import './ocrApp.css';

type OCRDataPoint = {
    image_name: string
    table_idx: string
    cell_id: string
    ocr_text: string
    human_text?: string
    image_path: string
    image_width: number
    image_height: number
}

type OCRFixerState = {
    ocrDataPoints?: OCRDataPoint[]
    fetchOCRDataPoints: () => void
}

const useStore = create<OCRFixerState>((set, get) => ({
    ocrDataPoints: undefined,
    fetchOCRDataPoints: async () => {
        const response = await fetch("/ocr/data_points")
        const ocrDataPoints = (await response.json())["data_points"]
        set({ocrDataPoints})
    }
}))


function OCRApp() {
    const fetchOCRDataPoints = useStore(state => state.fetchOCRDataPoints)
    const ocrDataPoints = useStore(state => state.ocrDataPoints)

    useEffect(() => {
        if(typeof(ocrDataPoints) === "undefined") {
            fetchOCRDataPoints()
        }
    })
    if(typeof(ocrDataPoints) != "undefined" && ocrDataPoints.length > 0) {
        return (
            <div className="App">
                {
                    ocrDataPoints.map((dataPoint, i) => {
                        return (<OCRFixItem key={i} dataPoint={dataPoint}/>)
                    })
                }
            </div>
        )
    } else if (typeof(ocrDataPoints) != "undefined" && ocrDataPoints.length === 0) {
        return (
            <div>There are no ocr data points to annotate...</div>
        )
    } else {
        return (
            <div>Still loading...</div>
        )
    }
}

function OCRFixItem(props: {dataPoint: OCRDataPoint}) {
    return (
        <div className="OCRFixItem">
            <img className="CellImage" src={props.dataPoint.image_path} width={props.dataPoint.image_width}
                 height={props.dataPoint.image_height} alt={`cell image ${props.dataPoint.image_path}`}/>
            <textarea className="OCRInput" rows={5} cols={50}>
                {props.dataPoint.human_text === null ?
                    props.dataPoint.ocr_text : props.dataPoint.human_text}
            </textarea>
            <div className="OCRStatusIndicator"
                 style={{background: props.dataPoint.human_text === null ? "yellow" : "green"}}/>
        </div>
    )
}

export default OCRApp;