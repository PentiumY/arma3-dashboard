<script>
  import Header from '$lib/components/Header.svelte';
  let bgUrl = '/background.png';
</script>

<Header current="" />

<div class="bg-gray-800 w-full min-h-screen">
  <div class="relative w-full h-96 bg-cover bg-center" style="background-image: url({bgUrl})">
    <h1 class="text-white text-3xl p-6 relative z-10">1988</h1>

    <!-- Fade overlay -->
    <div class="absolute bottom-0 left-0 w-full h-32 bg-linear-to-t from-gray-800 to-transparent z-20"></div>
  </div>
</div>


