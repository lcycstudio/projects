<template>
    <div id="map-container">
        <v-container>
            <div id="map-title" class="text-h4 pl-3">
                <span>Google Map</span>
                <v-btn id="map-location-btn" class="ma-2" size="small" color="primary" @click="getLocation">
                    Get My Location <v-icon end icon="mdi-crosshairs"></v-icon>
                </v-btn>
            </div>
            <div class="text-body-1 pl-4" v-if="thisText">Latest search: {{ thisText }} </div>
            <div class="text-body-1 pl-4" v-if="thisTime?.time">
                Local time:
                {{ thisTime?.time }}
                {{ thisTime?.date }}
                {{ thisTime?.gmt }}
                {{ thisTime?.timezone }}
            </div>
            <div class="text-body-1 pl-4" v-if="markerList?.length === 1">
                <div>Current Select: {{ markerList[0].location.name }}</div>
                <div>{{ markerList[0].location.formatted_address }}</div>
            </div>
            <v-container>
                <div id="vue-map"></div>
            </v-container>
        </v-container>
    </div>
</template>

<script lang="ts">
import { Loader } from '@googlemaps/js-api-loader';
import { LocationIF, DateTimeIF, SearchItemIF } from '@/interfaces/search';

export default {
    name: "Map Container",
    props: {
        searchText: String,
        markerList: Array<SearchItemIF>,
        searchTime: {
            type: Object as () => DateTimeIF,
        }
    },
    data() {
        return {
            loader: null as any,
            map: null as any,
            thisText: this.searchText,
            thisList: this.markerList,
            thisTime: this.searchTime,
            location: {} as LocationIF,
        }
    },
    emits: ['emitLocation'],
    setup(props, ctx) {
        ctx.emit('emitLocation')
    },
    methods: {
        getLocation: function () {
            if ("geolocation" in navigator) {
                navigator.geolocation.getCurrentPosition(
                    (position) => {
                        const lat = position.coords.latitude
                        const lng = position.coords.longitude
                        this.location = { lat: lat, lng: lng }
                        const thisLoader = this.loader as Loader
                        thisLoader
                            .load()
                            .then((google) => {
                                this.map = new google.maps.Map(
                                    document.getElementById("vue-map") as HTMLElement,
                                    {
                                        center: { lat: lat, lng: lng },
                                        zoom: 13,
                                        mapTypeId: 'roadmap',
                                    }
                                )
                                this.$emit('emitLocation', true)
                            })
                            .catch(error => {
                                alert(error);
                            });
                    },
                    (error) => {
                        alert('Error getting user location')
                    }
                )
            } else {
                alert("Geolocation is not supported by this browser.")
            }
        }
    },
    watch: {
        searchText: function (newValue, oldValue) {
            this.thisText = newValue ? newValue : oldValue;
        },
        markerList: function (newValue, _) {
            this.thisList = newValue
            if (newValue.length > 0) {
                const loader2 = this.loader as Loader
                loader2
                    .load()
                    .then((google) => {
                        let markers: any[] = []
                        const map = new google.maps.Map(
                            document.getElementById("vue-map") as HTMLElement,
                            {
                                center: this.location,
                                zoom: 13,
                                mapTypeId: 'roadmap',
                            }
                        )
                        const bounds = new google.maps.LatLngBounds();
                        newValue.forEach((place: any) => {
                            if (!place.location.geometry || !place.location.geometry.location) {
                                console.log("Returned place contains no geometry");
                                return;
                            }
                            const icon = {
                                url: place.location.icon as string,
                                size: new google.maps.Size(30, 30),
                                origin: new google.maps.Point(0, 0),
                                anchor: new google.maps.Point(17, 34),
                                scaledSize: new google.maps.Size(25, 25),
                                fillColor: place.location.icon_background_color
                            }
                            markers.push(
                                new google.maps.Marker({
                                    map,
                                    // icon,
                                    title: place.location.name,
                                    position: place.location.geometry.location
                                })
                            );
                            if (place.location.geometry.viewport) {
                                bounds.union(place.location.geometry.viewport);
                            } else {
                                bounds.extend(place.location.geometry.location);
                            }
                        })
                        map.fitBounds(bounds);
                    })
                    .catch(error => {
                        alert(error)
                    });
            } else {
                if (this.loader) {
                    const loader2 = this.loader as Loader
                    loader2
                        .load()
                        .then((google) => {
                            const map = new google.maps.Map(
                                document.getElementById("vue-map") as HTMLElement,
                                {
                                    center: this.location,
                                    zoom: 13,
                                    mapTypeId: 'roadmap',
                                }
                            )
                        })
                }
            }
        },
        searchTime: function (newValue, _) {
            this.thisTime = newValue
        },
    },
    mounted() {
        this.loader = new Loader({
            apiKey: import.meta.env.VITE_API_KEY!,
            version: "weekly",
            libraries: ["places"]
        })
        const thisLoader = this.loader as Loader
        thisLoader
            .load()
            .then((google) => {
                this.map = new google.maps.Map(
                    document.getElementById("vue-map") as HTMLElement,
                    {
                        center: { lat: 40.749933, lng: -73.98633 },
                        zoom: 13,
                        mapTypeId: 'roadmap',
                    }
                )
            })
            .catch(error => {
                alert(error);
            });
    }
}
</script>

<style>
#map-container {
    width: 60%;
    height: 600px;
}

#map-title {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

#vue-map {
    height: 400px;
}
</style>