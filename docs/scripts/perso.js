var counterProperties = {}
counterProperties[1] = {suffix:" reviews",number:22507155}
counterProperties[2] = {suffix:" products",number:2370585}
counterProperties[3] = {suffix:" unique reviewers",number:8026324}
counterProperties[4] = {suffix:" reviews",number:4607047}
counterProperties[5] = {suffix:" products",number:208321}
counterProperties[6] = {suffix:" unique reviewers",number:2088620}
counterProperties[7] = {suffix:" titles from wikipedia",number:1636}
counterProperties[8] = {suffix:" matchs",number:1243}
counterProperties[9] = {suffix:" finally kept",number:888}
counterProperties[10] = {suffix:" titles from wikipedia",number:2254}
counterProperties[11] = {suffix:" matchs",number:1276}
counterProperties[12] = {suffix:" finally kept",number:1042}

function triggerCounterData(identifier){
  let options = {
    useEasing: true,
    useGrouping: true,
    decimal: '.',
    prefix: '',
    suffix: counterProperties[identifier].suffix
  };

  let counter = new CountUp('counter'+identifier, 0, counterProperties[identifier].number, 0, 3.0, options);
  counter.start();
}

function isVisible(id) {
  let el = document.getElementById(id)
  let rect = el.getBoundingClientRect();
  return (rect.top >= 0) && (rect.bottom <= window.innerHeight);
}

var alreadytriggered = new Array(12).fill(false)
window.onscroll = function() {
  for(let i=0;i<12;i++){
    let counterid=i+1
    if (isVisible('counter'+counterid)) {
      if (!alreadytriggered[i]) {
      alreadytriggered[i] = true;
      triggerCounterData(counterid)
    }
    }
    else{
      alreadytriggered[i] = false;//To remove if we want to trigger only once
    }
  }

}
