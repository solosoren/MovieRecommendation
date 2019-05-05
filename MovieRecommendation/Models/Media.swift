//
//  Media.swift
//  MovieRecommendation
//
//  Created by Soren Nelson on 4/18/19.
//  Copyright © 2019 SORN. All rights reserved.
//

import Foundation

class Media: NSObject, MediaProtocol {
    
    var yID: Int
    var title: String
    var genres: [String]
    var features: vector
    var ratings: [Double]
    var imageURL: String?
    var imageData: Data?
    var avgRating: Double?
    var numRatings: Double?
    
    init(id: Int, title: String, genres: [String], features: vector, ratings: [Double]) {
        self.yID = id
        self.title = title
        self.genres = genres
        self.features = features
        self.ratings = ratings
    }
    
    override public var description: String {
        return String("ID: \(yID) \nTitle: \(title) \ngenre: \(genres) \nratings: \(ratings)")
    }
    
    func getImageData(completion:@escaping (Data?) -> ()) {
        if let imageData = imageData {
            completion(imageData)
            
        } else {
            if let imageString = imageURL,
                let url = URL(string: imageString) {
                
                DispatchQueue.global(qos: .background).async {
                    let data = try? Data(contentsOf: url)
                    self.imageData = data
                    completion(data)
                }
                
            } else { completion(nil) }
        }
    }
    
    func getAvgRating() -> Double {
        if let avgRating = avgRating {
            return avgRating
            
        } else {
            numRatings = 0.0
            var sum = 0.0
            for rating in ratings {
                if rating > 0.0 {
                    numRatings! += 1.0
                    sum += rating
                }
            }
            return sum / numRatings!
        }
    }
    
}
