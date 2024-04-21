//import UIKit

var greeting = "Hello, playground"


extension Sequence where Element: AdditiveArithmetic {
    func sum() -> Element {
        return self.reduce(.zero, +)
    }
}

struct Partition<T: BinaryInteger> {
    let components: [T]
    let size: T

    // no want lazy (and/or var), it's a struct!
    init(components: [T]) {
        self.components = components
        self.size = components.sum()
    }
}

let p = Partition(components: [1, 2])
print(p)

//p.size

//let pu = Partition<UInt8>(components: [1, 2])
//print(pu)

