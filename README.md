# unnamed sweater design thing

i keep trying to think of a pun on "yak shaving" and "yoke" but it's not coming together.

## data modeling

still trying to hammer this out.  i think a "colorwork panel" needs to be a separate thing from the "sweater" --- a sweater can have multiple colorwork panels, and i want to make sure colorwork info isn't lost when the sweater gets resized.  ideally also a colorwork panel should be generalizable to other types of motifs like lace work and cables (ew)

the "sweater" should be generalizable to both yoke and raglan style sweaters (fuck set-in sleeves all my homies hate set-in sleeves).  modeling all sweaters as bottom-up for now since inverting that is simple.

all measurements will be *stored* in terms of stitch count and converted to inches/centimeters/furlongs using the gauge for visualization purposes only; the GUI might start you off by inputting measurements but this is immediately converted to a stitch count which you can then tweak as desired (at this stage we may also want to run an optimization that tweaks bicep circumference, chest circumference, and armpit seam length slightly to suggest stitch counts that are evenly divisible by a reasonable panel width of 12-20 sts at its widest point).

colorwork panel is stored as a list of rows (lists) of stitches --- each stitch has a color and a type (knit, purl, yarnover, m1r/m1l, k2tog/ssk) and may increase, decrease, or not affect the stitch count.  this does not deal well with cables but i think adding special "i'm part of a cable" stitch types can deal with that and i hate knitting cables so i don't care at this stage.  we can see how it works and change it later.

ooh, or possibly --- a stitch has a "stitch count before" and a "stitch count after".  for knit stitch this is 1/1, for yarnover it's 0/1, for a M1R it's 1/2, and for a cable it might be 4/4.  that lets us model a cable as a single "stitch", which is good, and determine how each stitch affects stitch count _and_ if we're very clever which stitches from the previous row it uses (which may be useful for visualization later).  we can validate that a row of a colorwork panel "consumes" all stitches from the previous row and add extra placeholder knit stitches if it doesn't.  (maybe later i can add support for short rows inside the colorwork section but honestly why would you do that)

yoke sweater parameters:
* torso length (from armpit seam to start of hem ribbing, rnds)
* sleeve length (from armpit seam to start of cuff ribbing, rnds)
* torso circumference (at chest just under armpits, sts)
  - optionally: specify a different hip circumference (sts).  default to chest circumference
  - optionally: specify a waist circumference (sts) and waist distance from yoke/torso join (rnds)
* sleeve circumference (at bicep, sts)
* sleeve circumference (at wrist, sts) --- sleeve is generated with 2 decs/rnd evenly between wrist and bicep colorwork panels
* sleeve cuff rib length (rnds) --- default to like 2".  used mainly for computing overall sweater dimensions
* torso hem rib length (rnds) --- default to like 1".  ditto
* yoke depth (rnds)
* circumference at collar (sts)
* armpit seam length (sts)
* collar rib length (rnds) --- default to like 1"
* optionally: specify a rise for the back of the collar (an even number of short rows), to be compensated by more short rows under the chest colorwork panels or at the hem.

armpit sleeve length, sleeve circumference at bicep, and torso circumference at chest determine yoke circumference at base.  yoke circumference at base, yoke depth, and circumference at collar determine how much the yoke panels have to decrease; an optimizer should suggest several yoke panel sizes (width in sts at base) and tweak yoke params as needed.  user still needs to specify where the yoke decreases are, although we can suggest a sensible default.  what would be *really* slick is if we could also take the yoke decreases and visualize the decrease curve/shoulder shape.

raglan sweater parameters:
* the circumference of the top of the sleeve piece needs to be measured from top of shoulder to desired bottom of the armscye, _not_ around the bicep.  (i've learned my lesson.)  i think this can maybe be modeled by exactly the same code though
* the yoke always decreases 8 sts/rnd until the desired collar circumference is reached

colorwork panels following the above spec will be the full width of the raglan panels, i guess.  might make data entry a bit tedious/repetitive but that feels like a UI problem more than a data model problem.  also the only raglan sweater pattern i've ever followed is the embrace octopus sweater which actually works really well under that model :p

hm, it's just occurred to me that people with more ample chest sizes than my top-surgeried ass might want to have more stitches distributed to the front of the torso/yoke (i.e., sleeve joins not placed at the exact antipodes of the torso).  so maybe split that "torso circumference" measurement into a "front" and "back" stitchcount.
