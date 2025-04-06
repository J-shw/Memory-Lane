function loadVolumes(){
    fetch('analysis/volumes')
    .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(volumes => {
        console.log(volumes);
        volumes.forEach(volume => {
            loadVolumeStat(volume);
        });
    });
}

function loadVolumeStat(volume){
    fetch('analysis/volume_stats/'+volume.id)
    .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(stats => {
        console.log(volume.name);
        console.log(stats);
    });
}