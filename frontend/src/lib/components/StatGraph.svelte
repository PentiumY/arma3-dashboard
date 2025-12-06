<script lang="ts">
  import { onMount } from 'svelte';
  import Chart from 'chart.js/auto';

  export let label: string;
  export let color: string = 'rgb(59,130,246)'; // Tailwind blue-500
  export let value: number = 0;

  let canvas: HTMLCanvasElement;
  let chart: Chart;

  let dataPoints: number[] = [];
  let labels: string[] = [];

  onMount(() => {
    chart = new Chart(canvas, {
      type: 'line',
      data: {
        labels,
        datasets: [
          {
            label,
            data: dataPoints,
            borderColor: color,
            borderWidth: 2,
            pointRadius: 0,
            tension: 0.3,
          },
        ],
      },
      options: {
        animation: false,
        scales: {
          y: {
            min: 0,
            max: 100,
          },
        },
      },
    });
  });

  $: if (chart) {
    const now = new Date().toLocaleTimeString();
    labels.push(now);
    dataPoints.push(value);

    if (labels.length > 30) {
      labels.shift();
      dataPoints.shift();
    }

    chart.update();
  }
</script>

<div class="bg-gray-800 p-4 rounded shadow text-white">
  <h2 class="font-bold mb-2">{label}</h2>
  <canvas bind:this={canvas}></canvas>
</div>
