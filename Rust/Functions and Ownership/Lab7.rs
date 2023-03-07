fn main() {
    let first_string: &str = "hello ";
    let second_string: &str = "world";
    let combined: String = stringConcat(first_string, second_string);
    println!("{}", combined);

    let array = [2.2, 23.6, 34.342, 4.3];
    println!("{}", subArrayAverage(&array, (1,3)));
  
    let v = arraySignum(&[2,-55,4,-1,-45,3,0,45,0]);
    println!("{:?}", v);

}

fn stringConcat<'life>(first_str: &'life str, second_str: &'life str) -> String {

   let together: String = format!("{}{}", first_str, second_str);
  
  together
}

fn subArrayAverage(arr: &[f64], bound: (i32, i32)) -> f64 {

  let average = if bound.0 < 0 || bound.1 < 0 || bound.0 >= bound.1 || bound.1 > arr.len() as i32 {0.0}
                else { 
                  let sum = (arr[(bound.0 as usize)..(bound.1 as usize)].iter().sum::<f64>()) as f64;
                  let result = sum / ((bound.1 - bound.0) as f64);
                  result
                };
  average
}

fn arraySignum(arr: &[i32]) -> Vec<i8> {

  let mut vector: Vec<i8> = Vec::new();
  
  for n in arr.iter() {
    if n < &(0 as i32) {vector.push(-1)}
    else if n == &(0 as i32) {vector.push(0)}
    else {vector.push(1)};
  };
  vector
}
