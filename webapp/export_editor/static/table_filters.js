(function(){

const DEBOUNCE_MS = 100;

function text_matches(text, filter) {
  return text.toLowerCase().includes(filter.toLowerCase());
}

function debounce(fn, timeoutMs) {
  let timer_id = null;
  
  return function(...args) {
    // Stop the old call, if possible
    if (timer_id) { window.clearTimeout(timer_id); }

    timer_id = window.setTimeout(() => {
      fn.apply(null, args);
    }, timeoutMs);
  };
}

function filter_table(table, filter) {
  const FILTERED_CLASS = 'filtered';

  if (filter == '') {
    // restore all rows
    table.querySelectorAll('tbody tr').forEach(tr => {
      tr.classList.remove(FILTERED_CLASS);
    })

    return;
  }

  table.querySelectorAll('tbody tr').forEach(tr => {
    const matches_filter = [...tr.querySelectorAll('td, th')].some(td => {
      return text_matches(td.innerText, filter);
    });

    if (matches_filter) {
      tr.classList.remove(FILTERED_CLASS);
    } else {
      tr.classList.add(FILTERED_CLASS);
    }
  });
}

document.querySelectorAll('input.filter').forEach(input => {
  const table_sel = input.dataset.tableSelector;
  if (!table_sel) { return; }

  const main = input.closest('.main');
  if (!main) { return; }

  const tables = [...main.querySelectorAll(table_sel)];
  if (tables.length == 0) { return; }

  input.addEventListener('keyup', debounce(() => {
    tables.forEach(table => filter_table(table, input.value)); 
  }, DEBOUNCE_MS));
  
});

})()
