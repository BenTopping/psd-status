<script setup>
import { ref, computed, watchEffect, toRef } from 'vue'

const props = defineProps({
  monitor: {},
})

const currentMonitor = toRef(props, 'monitor')

</script>

<template>
    <div class="flex flex-col w-full max-w-[800px] p-3 mt-2 rounded-lg drop-shadow-md bg-white">
        <span class="flex mb-5 p-2 w-full border-b-2">
            <h2 class="text-lg w-full text-center font-semibold">{{ currentMonitor.name || 'New'}}</h2>
        </span>
        <div class="flex flex-col p-5 w-full gap-y-3">
            <div class="flex flex-col">
                <label class="px-3">Protocol</label>
                <select 
                    class="border-2 border-gray-300 rounded-lg p-2 text-black" 
                    v-model="currentMonitor.protocol"
                >
                    <option value='http'>http</option>
                    <option value='https'>https</option>
                </select>
            </div>
            <div class="flex flex-col">
                <label class="px-3">Target</label>
                <input class="border-2 border-gray-300 rounded-lg p-2 text-black" placeholder="www.test.com" v-model="currentMonitor.target"/>
            </div>
            <div class="flex flex-col">
                <label class="px-3">Poll interval</label>
                <select 
                    class="border-2 border-gray-300 rounded-lg p-2 text-black" 
                    v-model="currentMonitor.interval"
                >
                    <option value='60'>1m</option>
                    <option value='120'>2m</option>
                    <option value='300'>5m</option>
                    <option value='600'>10m</option>
                    <option value='1800'>30m</option>
                    <option value='3600'>1h</option>
                    <option value='86400'>24h</option>
                </select>
            </div>
            <div class="flex flex-col">
                <label class="px-3">Active?</label>
                <select 
                    class="border-2 border-gray-300 rounded-lg p-2 text-black" 
                    v-model="currentMonitor.active"
                >
                    <option value='true'>True</option>
                    <option value='false'>False</option>
                </select>
            </div>
        </div>
        <button
          class="mx-auto w-32 bg-sdb-400 p-2 my-2 text-white rounded-lg text-base"
        >
          Create
        </button>
    </div>
</template>

