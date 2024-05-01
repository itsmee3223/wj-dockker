install docker
build image scaler
- ```docker build -t my-scaler-image .```

install docker swarmpit (gunakan manual installation)
- install

```git clone https://github.com/swarmpit/swarmpit -b master```

```docker stack deploy -c swarmpit/docker-compose.yml swarmpit```

- stop dan remove
  
```docker stack rm swarmpit```


buat file konfigurasi
- bisa langsung di swarmpit
- jika manual commandnya dibawah ini

```docker config create alertmanager_config alertmanager.yml```

```docker config create prometheus_config prometheus.yml```

buat stack jalanin
- copas ke swarmpit
- atau jalanin manual

```docker stack deploy -c docker-compose.yml wj-wordpress```

user swarmpit ```admin123```

pass swarmpit ```admin123```
