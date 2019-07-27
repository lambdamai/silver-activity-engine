import Foundation

struct Organization: Codable {
    let title: String
    let link: String
    let head_title: String
    let head_name: String
    let inn: String
    let ogrn: String
    let reg_date: String
    let reg_cap: String?
    let status: String?
    let main_activity: String
    let main_activity_code: String
    let address: String
}
