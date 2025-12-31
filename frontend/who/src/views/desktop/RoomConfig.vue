<script setup>
    import router from "@/router";
    import { ref, onMounted, reactive, watch} from "vue";
    
    const maxPlayers = ref(6)
    const members = ref([])
    const activeMembers = ref(new Set())
    const messageCount = ref()
    const filters = reactive({
        min_date: null,
        max_date: null,
        min_time: null,
        max_time: null
    })

    async function hostConfig() {
        try {
            const payload = {
                max_players: maxPlayers.value,
                filter: {
                    members: [...activeMembers.value],
                    min_date: dateStringToObject(filters.min_date),
                    max_date: dateStringToObject(filters.max_date),
                    min_time: timeStringToObject(filters.min_time),
                    max_time: timeStringToObject(filters.max_time),
                }
            };

            const response = await fetch("http://localhost:8000/api/room/init",
            {     
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(payload)
            }
            )
            if (!response.ok) { throw new Error("Failed to init the room") }

            const data = await response.json()
            router.push({ path: "config" })
        } catch (error) {
            alert(error.message)
        }
    }
    
    async function getMembers() {
        try {
            const response = await fetch("http://localhost:8000/api/reader/get_members",
            {
                method : "GET"
            }
            )
            if (!response.ok) { throw new Error("Failed to get the members") }
            
            const data = await response.json()
            members.value = data
            activeMembers.value = new Set(data)
        } catch (error) {
            alert(error.message)
        }
    }
    
    async function toggleMember(name) {
        if (activeMembers.value.has(name)) {
            activeMembers.value.delete(name)
        } else {
            activeMembers.value.add(name)
        }
        getMessagesCount();
    }
    
    async function getMessagesCount() {
        try {
            const filterPayload = {
                members : [...activeMembers.value],
                min_date: dateStringToObject(filters.min_date),
                max_date: dateStringToObject(filters.max_date),
                min_time: timeStringToObject(filters.min_time),
                max_time: timeStringToObject(filters.max_time)  
            }
            
            const response = await fetch("http://localhost:8000/api/reader/get_messages_count",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(filterPayload)
            }
            )
            if (!response.ok) { throw new Error("Failed to get the number of messages") }
            
            const data = await response.json()
            messageCount.value = data
            
        } catch (error) {
            alert(error.message)
        }
    }
    
    // Auxiliar functions
    function dateStringToObject(date) {
        if (!date) return null
        
        const [year, month, day] = date.split('-').map(Number)
        return {day, month, year}
    }
    
    function timeStringToObject(time) {
        if (!time) return null
        
        const [hour, minute] = time.split(":").map(Number)
        return { hour, minute }
    }
    
    onMounted(async () => {
        await getMembers();
        await getMessagesCount();
    });

    watch(
    () => [
        filters.min_date,
        filters.max_date,
        filters.min_time,
        filters.max_time
    ],
    () => {
        getMessagesCount()
    }
    )
</script>

<template>
    <div class="page-center">
        <div class="members-card">
            <h1>Members Pool</h1>
            <button
            v-for="name in members"
            :key="name"
            :class="{ inactive: !activeMembers.has(name) }"
            @click="toggleMember(name)">
            {{ name }}
        </button>
        <p>
            You can <strong>select</strong> or <strong>deselect</strong> the members of the chat that you want to be in he game with your <strong>click</strong>
        </p>
    </div>
    <div class="invisible-card">
        <div class="text-stack">
            <strong>MAX PLAYERS:</strong>
            <input
            type="number"
            class="big-input"
            min="1"
            v-model="maxPlayers"/>
        </div>
        
        <div class="text-stack">
            <label>
                <strong>Min Date</strong>
                <input class="input-row" type="date" v-model="filters.min_date"/>
            </label>
            
            <label>
                <strong>Max Date</strong>
                <input class="input-row" type="date" v-model="filters.max_date" />
            </label>
        </div>
        
        <div class="text-stack">
            <label>
                <strong>Min Time</strong>
                <input class="input-row" type="time" v-model="filters.min_time" />
            </label>
            
            <label>
                <strong>Max Time</strong>
                <input class="input-row" type="time" v-model="filters.max_time" />
            </label>
        </div>
    </div>
    
    <div class="invisible-card">
        <p>There is <strong>{{ messageCount }} messages</strong> in the game</p>
        <button
        class="btn btn-secondary"
        @click="hostConfig()">
        HOST THE GAME
    </button>
</div>
</div>
</template>