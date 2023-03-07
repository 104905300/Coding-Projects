module Lab6 where 

  data RegularPoly = RegularPoly Int Float

  instance Eq RegularPoly where
    rp1 == rp2 = ((polyArea rp1 - polyArea rp2) < 1e-8)

  instance Show RegularPoly where
    show (RegularPoly numOfSide length) = 
      "Number of side(s): " ++ show(numOfSide) ++ "\nlength of each side: " ++       
        show(length)

  -- area = 0.5 * perimeter * (length/(2 * tan(180/number of side)))
  polyArea (RegularPoly numOfSide lengthOfSide) = do
    let side = fromIntegral numOfSide :: Float -- convert int to float
    0.5 * (side * lengthOfSide) * lengthOfSide/(2 * tan (pi/side))