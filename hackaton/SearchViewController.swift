import UIKit

class SearchViewController: UIViewController {
    
    @IBOutlet weak var searchTextField: UITextField!
    @IBOutlet weak var searchTableView: UITableView!
    @IBAction func findButtonTapped(_ sender: Any) {
        if searchTextField.text != "2301039358" {
            organization = Organization(title: "ооо \" эрик \"",
                                        link: "/id/183960",
                                        head_title: "директор",
                                        head_name: "залян толик гришаевич",
                                        inn: "2301039358",
                                        ogrn: "1022300515511",
                                        reg_date: "25 октября 1999 г.",
                                        reg_cap: "10 000 руб.",
                                        status: nil,
                                        main_activity: "47.75 торговля розничная косметическими и товарами личной гигиены в специализированных магазинах",
                                        main_activity_code: "477500",
                                        address: "353411, Краснодарский край, Анапский район, село Супсех, Советская улица, дом 70")
            searchTableView.reloadData()
        } else {
            organization = nil
        }
    }
    
    var organization: Organization?
    
    override func viewDidLoad() {
        super.viewDidLoad()
        searchTableView.delegate = self
        searchTableView.dataSource = self
        
        Gradient().setGradientToNavigationBar(viewController: self)
    }
}

extension SearchViewController: UITableViewDataSource, UITableViewDelegate {
    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return 9
    }
    
    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        let cell = tableView.dequeueReusableCell(withIdentifier: "cell")!
        let row = indexPath.row
        cell.textLabel?.text = ""
        cell.detailTextLabel?.text = ""
        if organization != nil {
            switch row {
            case 0:
                cell.detailTextLabel?.text = organization?.title
            case 1:
                cell.textLabel?.text = "ИНН:"
                cell.detailTextLabel?.text = organization?.inn
            case 2:
                cell.textLabel?.text = "ОГРН:"
                cell.detailTextLabel?.text = organization?.ogrn
            case 3:
                cell.textLabel?.text = "дата регистрации"
                cell.detailTextLabel?.text = organization?.reg_date
            case 4:
                cell.textLabel?.text = organization?.head_title
                cell.detailTextLabel?.text = organization?.head_name
            case 5:
                cell.textLabel?.text = "уставный капитал"
                cell.detailTextLabel?.text = organization?.reg_cap
            case 6:
                cell.textLabel?.text = "основной вид деятельности"
                cell.detailTextLabel?.text = organization?.main_activity
            case 7:
                cell.textLabel?.text = "адресс"
                cell.detailTextLabel?.text = organization?.address
            case 8:
                if organization?.status != nil {
                    cell.textLabel?.text = "статус:"
                    cell.detailTextLabel?.text = organization?.status
                }
            default: print("хуй")
            }
        }
        return cell
    }
}
