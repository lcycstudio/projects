<template>
  <v-app>
    <div id="app-container">
      <InfoContainer :hasLocation="hasLocation" @searchLocation="onSearchLocation" @filterLocation="onFilterLocation"
        @clearList="onClearList" />
      <MapContainer :searchText="searchText" :markerList="markerList" :searchTime="searchTime"
        @emitLocation="emitLocation" />
    </div>
  </v-app>
</template>

<script lang="ts">
import InfoContainer from '@/components/InfoContainer.vue';
import MapContainer from '@/components/MapContainer.vue';
import { DateTimeIF, SearchItemIF } from '@/interfaces/search';

export default {
  name: "DefaultComponent",
  components: {
    InfoContainer,
    MapContainer
  },
  data() {
    return {
      searchText: "" as string,
      markerList: [] as Array<SearchItemIF>,
      searchTime: {} as DateTimeIF,
      hasLocation: false,
    };
  },
  methods: {
    onSearchLocation: function (result: { text: string, time: Date, places: any }) {
      if (result) {
        this.searchText = result.text;
        this.searchTime = {
          time: result.time.toLocaleTimeString(),
          date: result.time.toDateString(),
          gmt: result.time.toTimeString().split(' ')[1],
          timezone: '(' + result.time.toTimeString().split('(')[1],
        }
        this.markerList = result.places.filter((item: any) => (item.value === 1))
      }
    },
    onFilterLocation: function (places: Array<SearchItemIF>) {
      if (places && places.length > 0) {
        this.markerList = places.filter((item) => (item.value === 1))
      }
    },
    onClearList: function () {
      this.markerList = []
      this.searchText = ''
    },
    emitLocation: function (res: boolean) {
      this.hasLocation = res
    }
  },
  mounted() {
    // if ("geolocation" in navigator) {
    //   navigator.geolocation.getCurrentPosition(
    //     (position) => {
    //       const lat = position.coords.latitude
    //       const lng = position.coords.longitude
    //       this.myLocation = { lat: lat, lng: lng }
    //     },
    //     (error) => {
    //       alert('Error getting user location')
    //     }
    //   )
    // } else {
    //   alert("Geolocation is not supported by this browser.")
    // }
  }
}
</script>

<style>
#app-container {
  display: flex;
  flex-direction: row;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 90%;
  border: 5px solid #d3d3d3;
  border-radius: 15px;
}
</style>
