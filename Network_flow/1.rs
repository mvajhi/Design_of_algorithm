use std::io::{self, BufRead};
use std::collections::VecDeque;

/// ساختار Edge که معادل کلاس edge در پایتون است
#[derive(Clone)]
struct Edge {
    to: usize,      // اندیس هدف
    capacity: i32,  // ظرفیت یال
    flow: i32,      // جریان عبوری از یال
}

/// ساختار Node که معادل کلاس Node در پایتون است
struct Node {
    edges: Vec<Edge>,
    is_full: bool,
}

/// تابع برای خواندن ورودی (مشابه read_input در پایتون)
fn read_input() -> (usize, Vec<Vec<char>>) {
    let stdin = io::stdin();
    let mut lines_iter = stdin.lock().lines();
    
    // خواندن مقدار n
    let n_line = lines_iter.next().unwrap().unwrap();
    let n: usize = n_line.trim().parse().unwrap();
    
    // خواندن گرید به اندازه 2*n - 1
    let mut grid = Vec::new();
    for _ in 0..(2 * n - 1) {
        let line = lines_iter.next().unwrap().unwrap();
        grid.push(line.chars().collect());
    }
    
    (n, grid)
}

/// تابع ساخت نودها و اتصال یال‌ها بر اساس منطق موجود در پایتون
fn create_nodes(n: usize, grid: &[Vec<char>]) -> (Vec<Node>, usize, usize) {
    // ایجاد source و sink
    let mut source = Node {
        edges: Vec::new(),
        is_full: true,
    };
    let mut sink = Node {
        edges: Vec::new(),
        is_full: true,
    };

    // ایجاد مجموعه نودها
    let mut nodes: Vec<Node> = Vec::new();
    for i in 0..n {
        for j in 0..n {
            let mut new_node = Node {
                edges: Vec::new(),
                is_full: true,
            };
            let is_left = (i + j) % 2 == 0;
            let i_grid = 2 * (i + 1) - 1;
            let j_grid = 2 * (j + 1) - 1;
            
            // محاسبه ظرفیت راس (count)
            let mut count = 0;
            let directions = [(-1, 0), (1, 0), (0, -1), (0, 1)];
            for (di, dj) in directions.iter() {
                let ni_grid = (i_grid as isize + di) as usize;
                let nj_grid = (j_grid as isize + dj) as usize;
                
                // بر اساس کد پایتون ، اگر کاراکتر | یا - بود ادامه می‌دهیم
                if grid[ni_grid][nj_grid] == '|' || grid[ni_grid][nj_grid] == '-' {
                    continue;
                }
                count += 1;
            }
            
            // اگر count - 1 > 0 بود، یال به source یا sink زده می‌شود
            if count - 1 > 0 {
                new_node.is_full = false;
                if is_left {
                    // یال از source به این نود
                    source.edges.push(Edge {
                        to: nodes.len() + 2, // +2 برای اینکه idx های source و sink را در فهرست کلی در نظر بگیریم
                        capacity: (count - 1) as i32,
                        flow: 0,
                    });
                } else {
                    // یال از این نود به sink
                    new_node.edges.push(Edge {
                        to: 1, // اندیس sink (که فعلاً نهایی مشخص می‌کنیم موقع بازگشت)
                        capacity: (count - 1) as i32,
                        flow: 0,
                    });
                }
            }
            
            nodes.push(new_node);
        }
    }

    // ایجاد یال‌های بین نودها و همچنین یال‌های مربوط به خارج از محدوده
    for i in 0..n {
        for j in 0..n {
            let index = i * n + j;
            // اگر نود قابل استفاده نبود، ادامه می‌دهیم
            if nodes[index].is_full {
                continue;
            }
            let is_left = (i + j) % 2 == 0;
            let i_grid = 2 * (i + 1) - 1;
            let j_grid = 2 * (j + 1) - 1;
            
            let directions = [(-1, 0), (1, 0), (0, -1), (0, 1)];
            let mut count_out_of_range = 0;
            for (di, dj) in directions.iter() {
                let ni_grid = (i_grid as isize + di) as usize;
                let nj_grid = (j_grid as isize + dj) as usize;
                // در پایتون: اگر | یا - بود، ادامه بده
                if grid[ni_grid][nj_grid] == '|' || grid[ni_grid][nj_grid] == '-' {
                    continue;
                }
                let ni = (i as isize + di) as isize;
                let nj = (j as isize + dj) as isize;
                
                // بررسی اینکه همسایه داخل محدوده است یا خیر
                if ni >= 0 && ni < n as isize && nj >= 0 && nj < n as isize {
                    let neighbor_index = (ni as usize) * n + (nj as usize);
                    // اگر نود همسایه is_full نباشد و نود فعلی is_left باشد
                    if is_left && !nodes[neighbor_index].is_full {
                        nodes[index].edges.push(Edge {
                            to: neighbor_index + 2, // +2 برای در نظر گرفتن منبع و مقصد در ایندکس
                            capacity: 1,
                            flow: 0,
                        });
                    }
                } else {
                    // خارج از محدوده
                    count_out_of_range += 1;
                }
            }
            
            if count_out_of_range > 0 {
                if is_left {
                    // یال به sink
                    nodes[index].edges.push(Edge {
                        to: 1, // اندیس sink
                        capacity: count_out_of_range as i32,
                        flow: 0,
                    });
                } else {
                    // یال از source به این نود
                    source.edges.push(Edge {
                        to: index + 2,
                        capacity: count_out_of_range as i32,
                        flow: 0,
                    });
                }
            }
        }
    }

    // اندیس source در بردار نهایی = 0
    // اندیس sink در بردار نهایی = 1
    // بقیه نودها از ایندکس 2 شروع می‌شوند
    // ترتیب در نهایت: [source, sink, nodes...]
    let mut all_nodes: Vec<Node> = Vec::with_capacity(nodes.len() + 2);
    // index 0 => source
    all_nodes.push(source);
    // index 1 => sink
    all_nodes.push(sink);
    // بقیه را اضافه می‌کنیم
    for node in nodes {
        all_nodes.push(node);
    }

    (all_nodes, 0, 1) // (همه نودها، ایندکس source، ایندکس sink)
}

/// تابع BFS که مسیری با ظرفیت باقیمانده مثبت بین مبدا و مقصد پیدا می‌کند
fn bfs_find_path(
    nodes: &Vec<Node>,
    source: usize,
    sink: usize,
) -> Vec<Option<(usize, usize)>> {
    let mut parent = vec![None; nodes.len()];
    let mut queue = VecDeque::new();
    queue.push_back(source);

    // در اینجا parent[v] = Some((u, e_index)) یعنی
    // نود v از نود u و یال با اندیس e_index در u.edges به دست آمده
    while let Some(u) = queue.pop_front() {
        for (e_index, e) in nodes[u].edges.iter().enumerate() {
            if e.capacity - e.flow > 0 && parent[e.to].is_none() && e.to != source {
                parent[e.to] = Some((u, e_index));
                if e.to == sink {
                    return parent;
                }
                queue.push_back(e.to);
            }
        }
    }
    parent
}

/// تابع ادموند کارپ برای محاسبه جریان ماکزیمم
fn edmond_karp(nodes: &mut Vec<Node>, source: usize, sink: usize) -> i32 {
    let mut max_flow = 0;
    
    loop {
        let parent_map = bfs_find_path(nodes, source, sink);
        if parent_map[sink].is_none() {
            // اگر به مقصد نرسیدیم، مسیر اشباع شده است و دیگر مسیری وجود ندارد
            break;
        }
        
        // پیدا کردن کمترین ظرفیت باقیمانده در مسیر
        let mut flow = i32::MAX;
        let mut current_node = sink;
        while current_node != source {
            let (u, e_idx) = parent_map[current_node].unwrap();
            let edge = &nodes[u].edges[e_idx];
            let remaining_capacity = edge.capacity - edge.flow;
            if remaining_capacity < flow {
                flow = remaining_capacity;
            }
            current_node = u;
        }
        
        // اعمال افزایش جریان در مسیر
        current_node = sink;
        while current_node != source {
            let (u, e_idx) = parent_map[current_node].unwrap();
            let edge_capacity = nodes[u].edges[e_idx].capacity;
            let edge_flow = nodes[u].edges[e_idx].flow;
            
            // افزایش جریان یال اصلی
            nodes[u].edges[e_idx].flow = edge_flow + flow;
            
            // اضافه یا به‌روزرسانی یال برعکس
            // بررسی می‌کنیم آیا یال برعکس از current_node به u وجود دارد یا خیر
            let mut reverse_found = false;
            for rev_e in &mut nodes[current_node].edges {
                if rev_e.to == u {
                    rev_e.flow -= flow;
                    reverse_found = true;
                    break;
                }
            }
            if !reverse_found {
                // اگر یال برعکس وجود ندارد، ایجادش می‌کنیم
                nodes[current_node].edges.push(Edge {
                    to: u,
                    capacity: 0,
                    flow: -flow,
                });
            }
            
            current_node = u;
        }
        
        max_flow += flow;
    }
    
    max_flow
}

/// تابع solve که معادل solve در پایتون است و ادموند کارپ را فراخوانی می‌کند
fn solve(nodes: &mut Vec<Node>, source: usize, sink: usize) -> i32 {
    edmond_karp(nodes, source, sink)
}

fn main() {
    // خواندن ورودی
    let (n, grid) = read_input();
    
    // طبق کد پایتون، به جای n، از n-1 استفاده می‌شود
    let (mut nodes, source, sink) = create_nodes(n - 1, &grid);
    
    // محاسبه و چاپ نتیجه
    let ans = solve(&mut nodes, source, sink);
    println!("{}", ans);
}