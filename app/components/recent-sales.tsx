import { Avatar, AvatarFallback, AvatarImage } from '../components/ui/avatar';

export function RecentSales() {
  return (
    <div className="space-y-8">
      <div className="flex items-center">
        <Avatar className="h-9 w-9">
          <AvatarImage src="/avatars/01.png" alt="Avatar" />
          <AvatarFallback>PR</AvatarFallback>
        </Avatar>
        <div className="ml-4 space-y-1">
          <p className="text-sm font-medium leading-none">Pink Rollex</p>
          <p className="text-xs text-muted-foreground">
            Bought by Makinde Ayomide
          </p>
        </div>
        <div className="ml-auto font-medium text-teal-600 text-xs">+₦1,999.00</div>
      </div>
      <div className="flex items-center">
        <Avatar className="h-9 w-9">
          <AvatarImage src="/avatars/01.png" alt="Avatar" />
          <AvatarFallback>BF</AvatarFallback>
        </Avatar>
        <div className="ml-4 space-y-1">
          <p className="text-sm font-medium leading-none">Boy Friend Jean [Red]</p>
          <p className="text-muted-foreground text-xs">
            Item returned by Makinde Ayomide
          </p>
        </div>
        <div className="ml-auto font-medium text-red-600 text-xs">-₦5,000.00</div>
      </div>
    </div>
  );
}
