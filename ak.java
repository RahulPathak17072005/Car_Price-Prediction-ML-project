class Solution {
    public int maximumSwap(int num) {
       StringBuilder sb=new StringBuilder();
       ArrayList<Integer> list = new ArrayList<>();
       String s=Integer.toString(num);
       for(int i=0;i<s.length();i++){
        list.add((int)s.charAt(i));
       }
       Collections.sort(list);
       Collections.reverse(list);
       for(int i=0;i<list.size();i++){
        sb.append(list.get(i));
       }
       String s2= sb.toString();

       return Integer.parseInt(s2);
    }
}