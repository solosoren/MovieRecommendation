//
//  ImportController.swift
//  MovieRecommendation
//
//  Created by Soren Nelson on 1/10/19.
//  Copyright © 2019 SORN. All rights reserved.
//

import Foundation

class ImportController {
    
    static let sharedInstance = ImportController()
    
    func addMedia<T: Media, U: UserProtocol>(_ media: [T], for users: [U], featureCount: Int) -> RecommenderModel {
        var RM = RecommenderModel(movieCount: media.count, userCount: users.count, featureCount: featureCount)
        
        for m in media {
            if m.features.count < featureCount {
                print("ERROR")
                // throw error
            }
            RM.updateX(at: m.yID - 1, 0..<featureCount, with: m.features)
        }
        
        for u in users {
            if u.ratings.count < media.count {
                print("ERROR")
                // throw error
            }
            for mID in 0..<u.ratings.count {
                RM.updateRatings(at: mID, u.id, with: u.ratings[mID])
            }
        }
        return RM
    }
    
}
