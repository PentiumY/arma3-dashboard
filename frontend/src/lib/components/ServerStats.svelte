<script lang="ts">
  import { onMount } from 'svelte';
  import StatGraph from '$lib/components/StatGraph.svelte';

  let stats = { cpu: 0, memory: 0, gpu: 5, ethernet: 0 };

  function generateMockStats() {
    stats = {
      cpu: Math.random() * 100,
      memory: Math.random() * 100,
      gpu: Math.random() * 100,
      ethernet: Math.random() * 500  // simulate Mbps
    };
  }

  onMount(() => {
    // Update every 1 second with fake data  
    const interval = setInterval(generateMockStats, 1000);
    return () => clearInterval(interval);
  });
</script>


<h1 class="text-2xl font-bold p-4">Server Performance</h1>

<div class="grid grid-cols-1 md:grid-cols-2 gap-4 p-4">
  <StatGraph label="CPU Usage" value={stats.cpu} color="rgb(239,68,68)" />        <!-- Red -->
  <StatGraph label="Memory Usage" value={stats.memory} color="rgb(34,197,94)" />  <!-- Green -->
  <StatGraph label="GPU Load" value={stats.gpu} color="rgb(59,130,246)" />        <!-- Blue -->
  <StatGraph label="Ethernet Mbps" value={stats.ethernet} color="rgb(234,179,8)" /> <!-- Yellow -->
</div>
