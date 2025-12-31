<script setup>
  import router from "@/router";
  import { ref } from "vue";

  const loading = ref(false)

  async function uploadChat(file) {
    if (!file) return
    loading.value = true

    const formData = new FormData()
    formData.append("file", file)

    try {
      const response = await fetch("http://localhost:8000/api/reader/upload_chat",
        {
          method: "POST",
          body: formData
        }
      )
      if (!response.ok) { throw new Error("Failed to upload chat") }

      const data = await response.json()
      router.push("host/room")

    } catch (error) {
      alert(error.message)
      loading.value = false
    }
  }
</script>

<template>
  <div v-if=!loading class="page-center">
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

  <div v-else class="page-center">
    <div class="dots-loader">
      <span></span>
      <span></span>
      <span></span>
      <span></span>
    </div>
  </div>
</template>




