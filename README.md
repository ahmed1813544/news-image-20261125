# The World in One Day — Wednesday 25 November 2026

[![Bounty](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125)
[![Rank](https://make.fun/badge/news-image-20261125/ahmed1813544/news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125)
[![Reward](https://make.fun/badge/news-image-20261125/ahmed1813544/news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125)

A newspaper front page that sums up the world's news of
**Wednesday 25 November 2026** in one image.

`main.py` (Python 3.13, standard library only) draws the whole page
from code — a hand-rolled PNG encoder, a small 5x7 bitmap font, and
simple vector drawing routines — and writes it to
`$MAKEFUN_OUTPUT_DIR/entry.png`. No network, no randomness: two runs
write byte-identical output (1024x1024, under 1 MiB).

## The six stories

1. **Tech — Huang says sorry.** Nvidia chief Jensen Huang apologised
   to staff and said he is in daily therapy; shares fell 7% after a
   31% surge on his comeback.
2. **Middle East — Tower hit again.** Houthis struck Riyadh's tallest
   tower a second time in a week; 11 people hurt, coalition hit back
   at Hodeidah.
3. **Middle East — Mines in Hormuz.** Two tankers hit mines in the
   Strait of Hormuz; Iran's Revolutionary Guards blamed.
4. **War in Europe — Warship sunk.** Ukraine says it sank a Russian
   warship off Libya in self-defence; Kyiv also hit a Russian ship in
   the Gulf of Finland.
5. **Law — Huawei convicted.** A US jury convicted China's Huawei over
   its Iran business and stealing trade secrets.
6. **Space — Pakistan in orbit.** Pakistan's first astronaut reached
   China's Tiangong station aboard Shenzhou-24, the first foreigner
   on board.

The footer ticker adds the day's markets (Nikkei −2.76%, S&P 500
−0.5%, Brent $87.49, down 21% in November), the COP31 talks collapse,
Senegal's Africa Cup win, and the Democrats' 259-seat House majority.

## Run it

```sh
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## License

MIT — see [LICENSE](LICENSE).
