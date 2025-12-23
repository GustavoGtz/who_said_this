<script setup>
import { ref } from "vue";

const state = ref("home")

async function uploadChat(file) {
  if (!file) return
  state.value = "loading"

  const formData = new FormData()
  formData.append("file", file)

  try {
    const response = await fetch("http://localhost:8000/api/load_chat",
      {
        method: "POST",
        body: formData
      }
    )

    if (!response.ok) {
      throw new Error("Failed to upload chat")
    }
    const data = await response.json()
    state.value = "loaded"

  } catch (error) {
    alert(error.message)
    state.value = "home"
  }
}

</script>

<template>
  <div v-if="state === 'home'" class="page-center">
    <div class="card">
      <h1>WHO SAID THIS?</h1>

      <p>Upload your friends WhatsApp Chat History to start the party</p>

      <label class="btn btn-primary">
        Load Chat
        <input
          type="file"
          hidden
          @change="e => uploadChat(e.target.files[0])"
        />
      </label>

      <p class="hint">
        <a
          href="https://faq.whatsapp.com/1180414079177245/?cms_platform=android"
          target="_blank"
          rel="noopener"
        >
          If you don't know how to get your WhatsApp Chat History
        </a>
      </p>
    </div>
  </div>

  <!-- LOADING -->
  <div v-else-if="state === 'loading'" class="page-center">
    <div class="dots-loader">
      <span></span>
      <span></span>
      <span></span>
      <span></span>
    </div>

  </div>

  <!-- NEXT -->
  <div v-else class="page-center">
    <div class="card">
      <h2>Chat loaded!</h2>
      <p>Ready to continue.</p>
    </div>
  </div>
</template>




