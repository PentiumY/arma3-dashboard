<script>
  let files = null;
  let uploading = false;
  let result = null;

  async function upload() {
    if (!files || !files.length) return;

    uploading = true;
    result = null;

    const form = new FormData();
    form.append("file", files[0]); // or append all if multiple

    const res = await fetch("http://127.0.0.1:8000/upload", {
      method: "POST",
      body: form
    });

    const data = await res.json();
    result = data;
    uploading = false;
  }
</script>

<div class="space-y-3">
  <!-- File input -->
  <label
    class="block w-full cursor-pointer rounded-xl border border-gray-300 bg-white px-4 py-3 text-sm text-gray-700 shadow-sm transition
           hover:bg-gray-50 focus-within:ring-2 focus-within:ring-blue-500"
  >
    <span>{files && files.length ? "Change file…" : "Select file…"}</span>
    <input type="file" class="sr-only" bind:files />
  </label>

  {#if files && files.length}
    <p class="text-sm text-gray-600 truncate">{files[0].name}</p>

    <button
      on:click={upload}
      class="px-4 py-2 rounded-lg bg-blue-600 text-white text-sm hover:bg-blue-700 disabled:opacity-50"
      disabled={uploading}
    >
      {uploading ? "Uploading…" : "Upload file"}
    </button>
  {/if}

  {#if result?.mods}
    <div class="space-y-2 mt-4">
            {#each result.mods as mod}
                <div class="p-3 bg-gray-100 rounded border">
                    <p class="font-semibold">{mod.name}</p>
                    <p class="text-sm text-gray-600">{mod.source}</p>
                    <a class="text-blue-600 text-sm" href={mod.url} target="_blank">
                        {mod.url}
                    </a>
                </div>
            {/each}
        </div>
    {/if}
</div>
