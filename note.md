start subprocess
it does it's own processing and start filling channel
then later own we start asking for data from that channel

make(chan, 3)
go start(channel)

<- channel: empty channel