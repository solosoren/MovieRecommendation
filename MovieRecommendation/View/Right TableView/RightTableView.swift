//
//  RightTableView.swift
//  MovieRecommendation
//
//  Created by Soren Nelson on 11/27/18.
//  Copyright © 2018 SORN. All rights reserved.
//

import Foundation
import Cocoa

class RightTableView: NSObject, NSTableViewDelegate, NSTableViewDataSource {
    
// MARK: TableView
    var tableView: NSTableView?
    var contentDelegate: UpdateContent?
    let MediaCellID = "MovieRatingCell"
    let CategoryCellID = "CategoryCell"
    let TitleCellID = "TitleCell"
    var titleCell: TitleCell?
    
    var selectedCategoryRow = 1
    var selectedCategory = Category(name: "All", count: 0)
    
    //    MARK: Tableview
    func setTableView(_ tableView: NSTableView) {
        self.tableView = tableView
        self.tableView!.dataSource = self
        self.tableView!.delegate = self
        self.tableView!.backgroundColor = NSColor(red: 0.1205, green: 0.1232, blue: 0.1287, alpha: 1)
        self.tableView!.reloadData()
    }
    
    func numberOfRows(in tableView: NSTableView) -> Int {
        if currentContent == .Ratings {
            // Title + ratings
            return 1 + UserController.sharedInstance.getRatingsCount()
            
        } else {
            // Title + "all categories" + categories
            return 1 + ObjectController.sharedInstance.getCategoryCount() 
        }
    }
    
    func tableView(_ tableView: NSTableView, heightOfRow row: Int) -> CGFloat {
        if row == 0 { return 90 }
        else if currentContent == .Categories { return 82 }
        return 153
    }
    
    func tableView(_ tableView: NSTableView, shouldSelectRow row: Int) -> Bool {
        if (row == 0) { return false }
        if currentContent == .Ratings { return true }
        else {
            let oldCell = tableView.view(atColumn: 0, row: selectedCategoryRow, makeIfNecessary: false) as! RightTVCategoryCell
            oldCell.deselect()
            
            let newCell = tableView.view(atColumn: 0, row: row, makeIfNecessary: false) as! RightTVCategoryCell
            newCell.select()
            
            selectedCategoryRow = row
            selectedCategory = newCell.category!
            contentDelegate?.selectedCategory(selectedCategoryRow, category: selectedCategory)
            
            return false
        }
    }
    
    func tableView(_ tableView: NSTableView, viewFor tableColumn: NSTableColumn?, row: Int) -> NSView? {
        switch row {
        case 0 :
            titleCell = getTitleCellView(tableView: tableView)
            return titleCell
            
        default :
            if currentContent == .Ratings {
                return getRatingCellView(tableView: tableView, row: row)
            } else {
                return getCategoryCellView(tableView: tableView, row: row)
            }
        }
    }
    
    //    MARK: Title Cell
    private func getTitleCellView(tableView: NSTableView) -> TitleCell? {
        let cell = tableView.makeView(withIdentifier: NSUserInterfaceItemIdentifier(rawValue: TitleCellID), owner: nil) as? TitleCell
        cell?.layer?.backgroundColor = CGColor(red: 0.13, green: 0.13, blue: 0.14, alpha: 1)

        cell!.setHeader(currentContent)
        cell!.toggleHideButtons(currentContent == .Categories)
        return cell
    }
    
    //    MARK: Rating Cell
    private func getRatingCellView(tableView: NSTableView, row: Int) -> NSView? {
        let cell = tableView.makeView(withIdentifier: NSUserInterfaceItemIdentifier(rawValue: MediaCellID), owner: nil) as! RightTVMediaCell
        cell.layer?.backgroundColor = CGColor(red: 0.13, green: 0.13, blue: 0.14, alpha: 1)
        
        guard let (media, rating) = UserController.sharedInstance.getMediaAndRating(for: row - 1) else { return nil }
        cell.userRating = rating
        cell.media = media
        return cell
    }
    
    //    MARK: Category Cell
    private func getCategoryCellView(tableView: NSTableView, row: Int) -> NSView? {
        let cell = tableView.makeView(withIdentifier: NSUserInterfaceItemIdentifier(rawValue: CategoryCellID), owner: nil) as! RightTVCategoryCell
        cell.category = ObjectController.sharedInstance.getCategory(at: row - 1)
        if row == 1  {  cell.selected = true  }
        return cell
    }
    
// MARK: Content
    
    var currentContent = Content.Ratings
    
    func changeContent(to content: Content) {
        currentContent = content
        titleCell!.toggleHideButtons(currentContent == .Categories)
        tableView?.reloadData()
    }
    
}
