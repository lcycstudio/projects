<template>
    <div id="info-container">
        <v-container id="get-location-container">
        </v-container>
        <v-container id="search-input-container">
            <v-text-field id="search-input" v-model="text" :loading="loading" density="compact" variant="solo"
                label="Search" append-inner-icon="mdi-magnify" clear-icon="mdi-close-circle" single-line clearable
                hide-details @click:append-inner="search" @click:clear="clearText"></v-text-field>
            <div class="text-body-2 py-2">{{ errorMsg }}</div>
        </v-container>
        <v-container>
            <div id="search-list-title-container">
                <div class="text-h6">Search Result</div>
                <v-btn color="red" size="small" @click="clearList">Clear List</v-btn>
            </div>
            <div v-if="!entireList || entireList.length === 0" class="py-4 text-center">Your search list is empty</div>
            <v-card class="my-4 mx-auto" v-if="currentList && currentList.length > 0" v-for="(item, index) in currentList"
                :key="index">
                <div class="search-item">
                    <div><v-checkbox v-model="item.checked" hide-details @click="toggleCheck(index, $event)"></v-checkbox>
                    </div>
                    <div class="search-item-text" @click="onSelectItem(index)">
                        <div class="font-weight-bold">{{ item.location.name }}</div>
                        <div class="text-body-2">{{ item.location.formatted_address }}</div>
                    </div>
                </div>
            </v-card>
            <v-pagination v-if="entireList.length > 0" class="pagination mb-2" v-model="page" :length="pages"
                :total-visible="5" @click="updatePage(page)"></v-pagination>
        </v-container>
    </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import { SearchItemIF } from '@/interfaces/search'
import { Loader } from '@googlemaps/js-api-loader';

export default defineComponent({
    name: "Info Container",
    props: {
        hasLocation: Boolean
    },
    data() {
        return {
            errorMsg: '' as string,
            loading: false,
            text: '',
            page: 1,
            pages: 1,
            pageSize: 10,
            listCount: 0,
            entireList: [] as Array<SearchItemIF>,
            currentList: [] as Array<SearchItemIF>,
            isLocated: this.hasLocation,
        }
    },
    emits: ['searchLocation', 'filterLocation', 'clearList'],
    setup(props, ctx) {
        ctx.emit('searchLocation')
        ctx.emit('filterLocation')
        ctx.emit('clearList')
    },
    methods: {
        search: function () {
            this.loading = true
            const keyboardEvent = new KeyboardEvent('keydown', {
                code: 'Enter',
                key: 'Enter',
                charCode: 13,
                keyCode: 13,
                view: window,
                bubbles: true
            });
            const myInput = document.getElementById('search-input') as HTMLInputElement
            myInput.dispatchEvent(keyboardEvent)
        },
        toggleCheck: function (index: number, event: PointerEvent) {
            const item = this.currentList![index]
            const target = event.target as HTMLInputElement
            const currentList = [
                ...this.currentList!.slice(0, index),
                { ...item, checked: target.checked, value: target.checked ? 1 : 0 },
                ...this.currentList!.slice(index + 1)
            ]
            this.currentList = currentList
            const myIndex = this.page === 1 ? index : (this.page - 1) * this.pageSize - 1 + index
            const entireList = [
                ...this.entireList!.slice(0, myIndex),
                { ...item, checked: target.checked, value: target.checked ? 1 : 0 },
                ...this.entireList!.slice(myIndex + 1)
            ]
            this.entireList = entireList
            this.$emit('filterLocation', currentList)
        },
        updatePage: function (pageIndex: number) {
            let start = (pageIndex - 1) * this.pageSize
            let end = pageIndex * this.pageSize
            this.page = pageIndex
            this.currentList = this.entireList.slice(start, end)
            this.$emit('searchLocation', { text: this.text, time: new Date(), places: this.currentList })
        },
        clearText: function () {
            this.text = ''
        },
        clearList: function () {
            this.$emit('clearList')
            this.text = ''
            this.currentList = []
            this.entireList = []
        },
        onSelectItem: function (index: number) {
            const items = Array.from(document.getElementsByClassName('search-item') as HTMLCollectionOf<HTMLElement>)
            items.forEach((element: HTMLElement, i: number) => {
                if (i !== index) {
                    if (element.style.border === '5px solid rgba(22, 119, 255, 0.8)') {
                        element.style.border = 'none';
                    }
                } else {
                    const thisBorder = element.style.border;
                    if (thisBorder === '5px solid rgba(22, 119, 255, 0.8)') {
                        element.style.border = 'none';
                        this.$emit('filterLocation', this.entireList)
                    } else {
                        element.style.border = '5px solid rgba(22, 119, 255, 0.8)';
                        this.$emit('filterLocation', [this.entireList![index]])
                    }
                }
            });
        },
        getSeachList: function (input: HTMLInputElement, places: any) {
            this.loading = true
            this.text = input.value
            if (places.length === 0) {
                this.errorMsg = 'Place is not found or invalid'
                this.loading = false
                return;
            }
            this.errorMsg = ''
            this.entireList = places.map((item: any) => ({
                location: item,
                checked: true,
                value: 1
            }))
            this.listCount = places.length
            this.pages = Math.ceil(places.length / 10)
            if (this.listCount < this.pageSize) {
                this.currentList = this.entireList
            } else {
                this.currentList = this.entireList?.slice(0, this.pageSize)
            }
            this.loading = false
            this.$emit('searchLocation', { text: this.text, time: new Date(), places: this.currentList })
        }
    },
    watch: {
        hasLocation: function (newValue, _) {
            if (newValue) {
                this.isLocated = newValue
            }
        }
    },
    mounted() {
        const loader = new Loader({
            apiKey: import.meta.env.VITE_API_KEY!,
            version: "weekly",
            libraries: ["places"]
        })
        loader
            .load()
            .then((google) => {
                const input = document.getElementById('search-input') as HTMLInputElement
                const options = {
                    fields: ["formatted_address", "geometry", "name"],
                    strictBounds: false,
                };
                const searchBox = new google.maps.places.SearchBox(input, options);
                searchBox.addListener("places_changed", () => {
                    const places = searchBox.getPlaces();
                    if (!this.isLocated) {
                        document.getElementById('map-location-btn')?.click();
                        setTimeout(() => {
                            this.getSeachList(input, places)
                        }, 500);
                    } else {
                        this.getSeachList(input, places)
                    }
                })
            })
            .catch(error => {
                alert(error)
            });
    }
})
</script>

<style>
#info-container {
    width: 40%;
    display: flex;
    flex-direction: column;
    align-items: center;
    height: 600px;
    overflow-y: auto;
}

#search-location-btn {
    width: 100%;
}

#search-list-title-container {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
}

#search-input-container {
    display: flex;
    flex-direction: column;
}

#search-input {
    width: 90%;
    padding: 10px;
    border-bottom: 1px solid rgb(211, 211, 211);
}

.search-item {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
}

.search-item:hover {
    border: 2px solid #d3d3d3;
}

.search-item-text {
    width: 80%;
}

.search-item-text:hover {
    cursor: pointer;
}

.delete-icons:hover {
    cursor: pointer;
}
</style>