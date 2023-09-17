export interface DateTimeIF {
    time: string,
    date: string,
    gmt: string,
    timezone: string
}

export interface LocationIF {
    lat: number,
    lng: number
}

export interface SearchItemIF {
    location: any,
    checked: boolean,
    value: number
}
