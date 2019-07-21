//
//  Expansion.swift
//  MovieRecommendation
//
//  Created by Soren Nelson on 2/6/19.
//  Copyright © 2019 SORN. All rights reserved.
//

import Foundation
import Cocoa

extension ViewController {
    
    private func toggleExpansion() {
        if !ViewController.isExpanded {
            expand()
            
        } else {
            minimize()
        }
        ViewController.isExpanded = !ViewController.isExpanded
        leftTableView.reloadData()
        rightTableView.reloadData()
    }
    
//    private func changeArrow(_ button: NSButton, to imageName: String) {
//        button.image = NSImage.init(named: imageName)
//    }

    private func minimize() {
        leftTVToViewConstraint.isActive = false
        leftTVToCategoriesConstraint.isActive = true
        
        rightTVToViewConstraint.isActive = false
        rightTVToCategoriesConstraint.isActive = true
        
        categoriesTableView.isHidden = false
    }
    
    private func expand() {
        leftTVToCategoriesConstraint.isActive = false
        
        leftTVToViewConstraint.constant = 66
        leftTVToViewConstraint.isActive = true
        
        rightTVToViewConstraint.constant = 66
        rightTVToViewConstraint.isActive = true
        
        categoriesTableView.isHidden = true
    }
    
    @IBAction func recExpandButtonPressed(_ sender: Any) {
        if !ViewController.isExpanded {
            rightDataSource.changeContent(to: Content.Categories)
            leftDataSource.toggleArrowButtonDirection()
            
        } else {
            leftDataSource.changeContent(to: Content.Recommendations)
            rightDataSource.changeContent(to: Content.Ratings)
            leftDataSource.toggleArrowButtonDirection()
        }
        toggleExpansion()
    }
    
    @IBAction func ratingsExpandButtonPressed(_ sender: Any) {
        toggleExpansion()
        leftDataSource.changeContent(to: Content.Ratings)
        rightDataSource.changeContent(to: Content.Categories)
        leftDataSource.toggleArrowButtonDirection()
    }
    
    func loadCategories() {
        
    }
    
}
